"""Restricted, conservative boss benchmark preparation for the oracle spike.

This is not a general build/uptime auditor. It admits the reviewed player-skill
family and plain stat jewels while keeping gear, gems and allocation choices fixed.
"""

import math
import re
from typing import Any
from xml.etree import ElementTree as ET

from exileai.pob.validation import UnsupportedBuild, active_import_nodes

POLICY = "conservative-boss-conditions-v1"
BOOLEAN_SETTINGS = {
    "conditionEnemyDazed",
    "conditionChilledEnemyRecently",
    "conditionIgnitedEnemyRecently",
    "conditionEnemyBlinded",
    "conditionEnemyIgnited",
    "conditionEnemyChilled",
    "conditionEnemyShocked",
    "conditionCritRecently",
    "conditionCritInPast8Sec",
    "conditionShockedEnemyRecently",
    "conditionKilledRecently",
    "conditionKilledShockedLast3Seconds",
    "conditionBeenHitRecently",
    "usePowerCharges",
}
ZERO_SETTINGS = {
    "conditionShockEffect",
    "configResonanceCount",
    "multiplierRage",
    "multiplierCombo",
}
QUEST_REWARDS = {
    "questAct 4Eye of HinekoraTribal Medicine": "30% increased Global Armour, Evasion and Energy Shield",
    "questAct 4Halls Of The DeadTawhoa's Test": "+5% to Lightning Resistance",
    "questAct 4Halls Of The DeadNgamahu's Test": "+5% to Fire Resistance",
    "questAct 4Abandoned PrisonGoddess of Justice": "30% increased Life Recovery from Flasks",
    "questInterlude 2QimahSeven Pillars": "15% increased Global Armour, Evasion and Energy Shield",
    "questAct 2Valley of the TitansMedallion": "30% increased Charm Charges Gained  +1 Charm Slot",
    "questAct 4Halls Of The DeadTasalio's Test": "+5% to Cold Resistance",
    "questAct 3Venom CryptsVenom Draught": "25% increased Stun Threshold",
}
ACTIVE_SKILLS = {
    "HollowFocusPlayer",
    "HollowResonancePlayer",
    "TrinityPlayer",
    "ChargedStaffPlayer",
    "TempestBellPlayer",
    "KillingPalmPlayer",
    "HeraldOfAshPlayer",
    "WhirlingAssaultPlayer",
    "WindDancerPlayer",
}


def validate_fixed_inputs(before_xml: str, after_xml: str) -> None:
    """Reject accidental non-passive changes in the engine's exported candidate."""
    before, after = ET.fromstring(before_xml), ET.fromstring(after_xml)
    for tag in ("Build", "Skills", "Items", "Config", "Party"):
        left, right = before.find(tag), after.find(tag)
        if left is None or right is None:
            if left is not None or right is not None:
                raise RuntimeError(f"fixed section changed: {tag}")
            continue
        if tag == "Build":
            # PlayerStat/MinionStat children cache outputs and must change with DPS.
            same = left.attrib == right.attrib
        else:
            same = ET.canonicalize(
                ET.tostring(left, encoding="unicode"), strip_text=True
            ) == ET.canonicalize(
                ET.tostring(right, encoding="unicode"), strip_text=True
            )
        if not same:
            raise RuntimeError(f"fixed section changed: {tag}")
    left_specs, right_specs = before.findall("Tree/Spec"), after.findall("Tree/Spec")
    if len(left_specs) != len(right_specs):
        raise RuntimeError("fixed tree specification count changed")
    for left_spec, right_spec in zip(left_specs, right_specs, strict=True):
        if {k: v for k, v in left_spec.attrib.items() if k != "nodes"} != {
            k: v for k, v in right_spec.attrib.items() if k != "nodes"
        }:
            raise RuntimeError("fixed class/ascendancy/tree choices changed")
        for tag in ("Sockets", "Overrides"):
            left, right = left_spec.find(tag), right_spec.find(tag)
            left_text = (
                ET.canonicalize(ET.tostring(left, encoding="unicode"), strip_text=True)
                if left is not None
                else None
            )
            right_text = (
                ET.canonicalize(ET.tostring(right, encoding="unicode"), strip_text=True)
                if right is not None
                else None
            )
            if left_text != right_text:
                raise RuntimeError(f"fixed passive choices changed: {tag}")


def validate_benchmark_build(xml: str) -> list[int]:
    """Admit a restricted fixed-mechanics build; runtime still verifies legality."""
    nodes = active_import_nodes(xml)
    root = ET.fromstring(xml)
    specs = root.findall("Tree/Spec")
    if len(specs) != 1:
        raise UnsupportedBuild("Benchmark requires one tree")
    spec = specs[0]
    if any(x.tag.startswith("WeaponSet") for x in spec) or bool(
        spec.get("masteryEffects")
    ):
        raise UnsupportedBuild(
            "Weapon-set branches and masteries require separate validation"
        )
    if any(x.tag not in {"URL", "Sockets", "Overrides"} for x in spec):
        raise UnsupportedBuild("Unsupported tree extension")
    if any(x.tag != "AttributeOverride" for x in spec.findall("Overrides/*")):
        raise UnsupportedBuild("Unsupported passive override")
    if root.findall("Party/*") or any(
        (x.text or "").strip() for x in root.findall(".//CustomModifierBlock")
    ):
        raise UnsupportedBuild("Party and custom modifiers require separate validation")
    skills = root.find("Skills")
    build = root.find("Build")
    if skills is None or build is None:
        raise UnsupportedBuild("Missing skill metadata")
    sets = skills.findall("SkillSet")
    if len(sets) != 1 or sets[0].get("id") != skills.get("activeSkillSet"):
        raise UnsupportedBuild("Benchmark requires one active skill set")
    groups = sets[0].findall("Skill")
    try:
        group_index = int(build.attrib["mainSocketGroup"]) - 1
        if not 0 <= group_index < len(groups):
            raise ValueError("Invalid group")
        main = groups[group_index]
    except (KeyError, ValueError) as error:
        raise UnsupportedBuild("Invalid main skill group") from error
    gem = main.find("Gem")
    if (
        main.get("enabled") != "true"
        or main.get("mainActiveSkill") != "1"
        or gem is None
        or gem.get("skillId") != "WhirlingAssaultPlayer"
        or gem.get("enabled") != "true"
    ):
        raise UnsupportedBuild(
            "Benchmark requires enabled Whirling Assault as the main skill"
        )
    for group in groups:
        first_gem = group.find("Gem")
        if first_gem is None or first_gem.get("skillId", "") not in ACTIVE_SKILLS:
            raise UnsupportedBuild("Unreviewed skill family")
    items = {x.get("id"): x for x in root.findall("Items/Item")}
    for socket in spec.findall("Sockets/Socket"):
        item = items.get(socket.get("itemId"))
        if item is None:
            raise UnsupportedBuild("Missing socketed jewel")
        lines = [s.strip() for s in (item.text or "").splitlines() if s.strip()]
        if len(lines) < 3 or lines[0] != "Rarity: RARE" or lines[2] != "Sapphire":
            raise UnsupportedBuild(
                "Only reviewed plain rare Sapphire jewels are supported"
            )
        patterns = (
            r"Item Level: \d+",
            r"LevelReq: \d+",
            r"Implicits: 0",
            r"\d+% increased maximum Energy Shield",
            r"\d+% increased Critical Damage Bonus",
            r"Recover \d+% of maximum Mana on Kill",
            r"\d+% increased Area of Effect",
        )
        if any(not any(re.fullmatch(p, line) for p in patterns) for line in lines[3:]):
            raise UnsupportedBuild("Jewel modifier requires separate validation")
    return nodes


def prepare_boss_benchmark(xml: str) -> tuple[str, dict[str, Any]]:
    """Normalize only reviewed configuration inputs, recording every override."""
    validate_benchmark_build(xml)
    root = ET.fromstring(xml)
    config = root.find("Config")
    if config is None or len(config.findall("ConfigSet")) != 1:
        raise UnsupportedBuild("Benchmark requires one configuration set")
    config_set = config.find("ConfigSet")
    assert config_set is not None
    if config_set.get("id") != config.get("activeConfigSet") or any(
        x.tag != "ConfigSet" for x in config
    ):
        raise UnsupportedBuild("Unsupported legacy or inactive configuration")
    target: dict[str, tuple[str, str]] = {
        key: ("boolean", "false") for key in BOOLEAN_SETTINGS
    }
    target.update({key: ("number", "0") for key in ZERO_SETTINGS})
    target.update(
        {
            "conditionEnemyIsolated": ("boolean", "true"),
            "enemyDistance": ("number", "20"),
        }
    )
    settings: list[dict[str, Any]] = []
    imported: dict[str, str] = {}
    for child in list(config_set):
        name = child.get("name", "")
        if child.tag == "Placeholder":
            if child.get("string") is not None:
                raise UnsupportedBuild("String placeholder requires separate audit")
            settings.append(
                {
                    "name": name,
                    "before": dict(child.attrib),
                    "after": "fresh-engine-default",
                    "reason": "reset-imported-placeholder",
                }
            )
            config_set.remove(child)
            continue
        if child.tag != "Input" or name in imported:
            raise UnsupportedBuild("Unknown or duplicate configuration entry")
        value_keys = set(child.attrib) - {"name"}
        if len(value_keys) != 1 or not value_keys <= {"string", "number", "boolean"}:
            raise UnsupportedBuild("Invalid configuration input type")
        key = next(iter(value_keys))
        value = child.attrib[key]
        if key == "boolean" and value not in {"true", "false"}:
            raise UnsupportedBuild("Invalid boolean configuration input")
        if key == "number":
            try:
                if not math.isfinite(float(value)):
                    raise ValueError("Non-finite number")
            except ValueError as error:
                raise UnsupportedBuild("Invalid numeric configuration input") from error
        imported[name] = value
        if name in QUEST_REWARDS:
            if key != "string" or value != QUEST_REWARDS[name]:
                raise UnsupportedBuild("Unreviewed quest reward")
            settings.append(
                {
                    "name": name,
                    "before": value,
                    "after": value,
                    "reason": "preserved-quest-reward",
                }
            )
        elif name in target:
            if key != target[name][0]:
                raise UnsupportedBuild("Unexpected conditional input type")
            config_set.remove(child)
        else:
            raise UnsupportedBuild(f"Configuration needs audit: {name}")
    for name, (kind, value) in sorted(target.items()):
        ET.SubElement(config_set, "Input", {"name": name, kind: value})
        reason = "unverified-uptime-disabled"
        if name in {"conditionKilledRecently", "conditionKilledShockedLast3Seconds"}:
            reason = "no-adds-boss-kill-effects-disabled"
        elif name == "conditionEnemyIsolated":
            reason = "standardized-no-adds-encounter"
        elif name == "enemyDistance":
            reason = "standardized-two-metre-distance"
        settings.append(
            {
                "name": name,
                "before": imported.get(name),
                "after": value,
                "reason": reason,
            }
        )
    return ET.tostring(root, encoding="unicode", xml_declaration=True), {
        "policy": POLICY,
        "settings": settings,
        "limitations": [
            "Conservative static PoB scenario, not measured sustained combat DPS",
            "Enabled skills, supports and intrinsic engine effects remain fixed; rotations and buff uptime are not simulated",
            "Only reviewed skill family, quest choices and plain stat jewels admitted",
        ],
    }
