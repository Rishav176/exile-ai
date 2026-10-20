"""The restricted benchmark must expose changes, not silently bless imports."""

from pathlib import Path
from xml.etree import ElementTree

import pytest

from exileai.pob.codec import decode_build_code
from exileai.pob.validation import UnsupportedBuild


def monk_xml() -> str:
    return decode_build_code(
        (
            Path(__file__).parent / "fixtures/monk-whirling-assault-contributed.pobcode"
        ).read_text()
    )


def test_conservative_benchmark_preserves_mechanics_and_reports_assumptions() -> None:
    from exileai.pob.benchmark import prepare_boss_benchmark

    original = ElementTree.fromstring(monk_xml())
    xml, audit = prepare_boss_benchmark(monk_xml())
    normalized = ElementTree.fromstring(xml)
    for section in ("Build", "Tree", "Skills", "Items"):
        before, after = original.find(section), normalized.find(section)
        assert before is not None and after is not None
        assert ElementTree.tostring(before) == ElementTree.tostring(after)
    values = {
        x.attrib["name"]: x.attrib for x in normalized.findall("Config/ConfigSet/Input")
    }
    assert values["conditionKilledRecently"]["boolean"] == "false"
    assert values["usePowerCharges"]["boolean"] == "false"
    assert values["multiplierRage"]["number"] == "0"
    assert values["conditionEnemyIsolated"]["boolean"] == "true"
    assert values["enemyDistance"]["number"] == "20"
    assert (
        values["questAct 3Venom CryptsVenom Draught"]["string"]
        == "25% increased Stun Threshold"
    )
    assert audit["policy"] == "conservative-boss-conditions-v1"
    assert any(
        x["name"] == "conditionKilledRecently"
        and x["before"] == "true"
        and x["after"] == "false"
        for x in audit["settings"]
    )
    assert normalized.findall(".//Config//Placeholder") == []


@pytest.mark.parametrize("value", ["maybe", "1", "", "True"])
def test_malformed_conditional_booleans_fail_instead_of_being_certified(
    value: str,
) -> None:
    from exileai.pob.benchmark import prepare_boss_benchmark

    root = ElementTree.fromstring(monk_xml())
    setting = next(
        x
        for x in root.findall("Config/ConfigSet/Input")
        if x.get("name") == "usePowerCharges"
    )
    setting.set("boolean", value)
    with pytest.raises(UnsupportedBuild, match="boolean"):
        prepare_boss_benchmark(ElementTree.tostring(root, encoding="unicode"))


@pytest.mark.parametrize(
    "change",
    [
        "weapon-set",
        "unique-jewel",
        "radius-jewel",
        "custom",
        "minion",
        "unknown-setting",
        "duplicate-setting",
        "quest",
        "missing-skills",
    ],
)
def test_unreviewed_mechanics_and_assumptions_fail_closed(change: str) -> None:
    from exileai.pob.benchmark import prepare_boss_benchmark

    root = ElementTree.fromstring(monk_xml())
    spec = root.find("Tree/Spec")
    config = root.find("Config/ConfigSet")
    assert spec is not None and config is not None
    if change == "weapon-set":
        ElementTree.SubElement(spec, "WeaponSet1", {"nodes": "1"})
    elif change in {"unique-jewel", "radius-jewel"}:
        jewel = next(x for x in root.findall("Items/Item") if x.get("id") == "3")
        assert jewel.text is not None
        jewel.text = (
            jewel.text.replace("RARE", "UNIQUE")
            if change == "unique-jewel"
            else jewel.text + "\nRadius: Large"
        )
    elif change == "custom":
        ElementTree.SubElement(root, "CustomModifierBlock").text = "100% more Damage"
    elif change == "minion":
        gem = root.find("Skills/SkillSet/Skill/Gem")
        assert gem is not None
        gem.set("skillId", "SkeletalWarriorPlayer")
    elif change == "unknown-setting":
        ElementTree.SubElement(
            config, "Input", {"name": "customMods", "string": "100% more Damage"}
        )
    elif change == "duplicate-setting":
        ElementTree.SubElement(
            config, "Input", {"name": "usePowerCharges", "boolean": "true"}
        )
    elif change == "quest":
        next(
            x for x in config if x.get("name") == "questAct 3Venom CryptsVenom Draught"
        ).set("string", "100% more Damage")
    elif change == "missing-skills":
        skills = root.find("Skills")
        assert skills is not None
        root.remove(skills)
    with pytest.raises(UnsupportedBuild):
        prepare_boss_benchmark(ElementTree.tostring(root, encoding="unicode"))


@pytest.mark.parametrize("value", ["nan", "inf", "bad"])
def test_invalid_numeric_assumptions_are_rejected(value: str) -> None:
    from exileai.pob.benchmark import prepare_boss_benchmark

    root = ElementTree.fromstring(monk_xml())
    setting = next(
        x
        for x in root.findall("Config/ConfigSet/Input")
        if x.get("name") == "multiplierRage"
    )
    setting.set("number", value)
    with pytest.raises(UnsupportedBuild, match="numeric"):
        prepare_boss_benchmark(ElementTree.tostring(root, encoding="unicode"))


def test_mutation_guard_rejects_equipment_or_ascendancy_changes() -> None:
    from exileai.pob.benchmark import validate_fixed_inputs

    xml = monk_xml()
    validate_fixed_inputs(xml, xml)
    for old, new in [
        ("24% increased maximum Energy Shield", "99% increased maximum Energy Shield"),
        ('ascendClassId="1"', 'ascendClassId="2"'),
    ]:
        assert old in xml
        with pytest.raises(RuntimeError, match="fixed"):
            validate_fixed_inputs(xml, xml.replace(old, new))
