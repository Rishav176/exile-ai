"""Deliberately narrow supported-input checks for the Spark integration spike."""

from xml.etree import ElementTree


class UnsupportedBuild(ValueError):
    """The spike cannot evaluate this build without additional validation."""


def active_import_nodes(xml: str) -> list[int]:
    """Validate versions and select the active tree for read-only inspection."""
    root = ElementTree.fromstring(xml)
    build = root.find("Build")
    tree = root.find("Tree")
    if root.tag != "PathOfBuilding2" or build is None or tree is None:
        raise UnsupportedBuild("Missing PoB2 build metadata")
    if build.get("targetVersion") != "0_1":
        raise UnsupportedBuild(
            "Unsupported target version; automatic conversion disabled"
        )
    specs = tree.findall("Spec")
    try:
        index = int(tree.get("activeSpec", "1")) - 1
        if not 0 <= index < len(specs):
            raise ValueError("Invalid active specification")
        spec = specs[index]
        if spec.get("treeVersion") != "0_5":
            raise UnsupportedBuild("Unsupported active tree version")
        nodes = sorted(int(value) for value in spec.attrib["nodes"].split(","))
        if not nodes or len(nodes) != len(set(nodes)):
            raise ValueError("Invalid allocation IDs")
        return nodes
    except (ValueError, KeyError) as error:
        raise UnsupportedBuild("Invalid active tree allocation") from error


def validate_spike_xml(xml: str) -> list[int]:
    root = ElementTree.fromstring(xml)
    build = root.find("Build")
    specs = root.findall("Tree/Spec")
    if root.tag != "PathOfBuilding2" or build is None:
        raise UnsupportedBuild("Missing PoB2 build metadata")
    if build.get("targetVersion") != "0_1":
        raise UnsupportedBuild(
            "Unsupported target version; automatic conversion disabled"
        )
    if len(specs) != 1 or specs[0].get("treeVersion") != "0_5":
        raise UnsupportedBuild("Spike requires one 0_5 tree specification")
    spec = specs[0]
    if spec.find("Sockets/Socket") is not None or any(
        child.tag.startswith("WeaponSet") for child in spec
    ):
        raise UnsupportedBuild("Jewel and weapon-set allocations are unsupported")
    if spec.get("masteryEffects", ""):
        raise UnsupportedBuild("Mastery choices are unsupported")
    if any(
        (block.text or "").strip() for block in root.findall(".//CustomModifierBlock")
    ):
        raise UnsupportedBuild("Custom modifiers require a separate audit")
    if root.find("Party/Build") is not None:
        raise UnsupportedBuild("Party imports require a separate audit")
    supported = {"enemyIsBoss", "enemyLevel", "enemyDamageType"}
    for setting in root.findall(".//Config//Input") + root.findall(
        ".//Config//Placeholder[@string]"
    ):
        if setting.get("name") not in supported:
            raise UnsupportedBuild(f"Configuration needs audit: {setting.get('name')}")
    gems = root.findall("Skills/SkillSet/Skill/Gem")
    if len(gems) != 1 or gems[0].get("skillId") != "SparkPlayer":
        raise UnsupportedBuild("Initial spike supports a single Spark gem only")
    try:
        nodes = sorted(int(value) for value in spec.attrib["nodes"].split(","))
    except (KeyError, ValueError) as error:
        raise UnsupportedBuild("Missing or invalid allocated node IDs") from error
    if not nodes or len(nodes) != len(set(nodes)):
        raise UnsupportedBuild("Empty or duplicate allocation IDs")
    return nodes


def validate_spike_scenario(scenario: object) -> None:
    expected = {
        "id": "solo-sustained-pinnacle-v1",
        "config": {
            "enemyIsBoss": "Pinnacle",
            "enemyLevel": 82,
            "enemyDamageType": "Average",
        },
    }
    if scenario != expected:
        raise UnsupportedBuild(
            "Unsupported scenario configuration; the versioned spike preset is fixed"
        )
