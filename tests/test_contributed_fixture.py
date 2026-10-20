import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree

import pytest

from exileai.pob.codec import decode_build_code
from exileai.pob.validation import (
    UnsupportedBuild,
    active_import_nodes,
    validate_spike_xml,
)
from scripts.curate_build import anonymize_xml


def test_anonymization_removes_identity_metadata_without_altering_inputs() -> None:
    xml = '<PathOfBuilding2><Build className="Mercenary" level="90"/><Notes>private</Notes><Import lastCharacterHash="secret"/><Skills><Skill label="personal"><Gem skillId="SparkPlayer"/></Skill></Skills><Config><Input name="customMods" string="150% increased cost efficiency"/></Config></PathOfBuilding2>'
    sanitized = ElementTree.fromstring(anonymize_xml(xml))
    assert sanitized.find("Notes") is None
    assert sanitized.find("Import") is None
    skill = sanitized.find("Skills/Skill")
    gem = sanitized.find("Skills/Skill/Gem")
    config = sanitized.find("Config/Input")
    assert skill is not None and skill.get("label") is None
    assert gem is not None and gem.get("skillId") == "SparkPlayer"
    assert (
        config is not None and config.get("string") == "150% increased cost efficiency"
    )


def test_anonymization_removes_item_identity_but_preserves_modifiers() -> None:
    xml = '<PathOfBuilding2><Items><Item id="1">Rarity: RARE\nRuby\nUnique ID: traceable\n15% increased Fire Damage\n</Item></Items></PathOfBuilding2>'
    sanitized = anonymize_xml(xml)
    assert "traceable" not in sanitized
    assert "15% increased Fire Damage" in sanitized


def test_real_fixture_preserves_active_tree_and_documents_exclusions() -> None:
    fixtures = Path(__file__).parent / "fixtures"
    xml = decode_build_code(
        (fixtures / "gemling-spark-contributed.pobcode").read_text()
    )
    metadata = json.loads(
        (fixtures / "gemling-spark-contributed.provenance.json").read_text()
    )
    assert hashlib.sha256(xml.encode()).hexdigest() == metadata["xml_sha256"]
    root = ElementTree.fromstring(xml)
    assert root.find("Import") is None
    assert root.find("Notes") is None
    assert len(active_import_nodes(xml)) == 132
    assert metadata["benchmark_eligible"] is False
    with pytest.raises(UnsupportedBuild):
        validate_spike_xml(xml)


def test_whirling_assault_fixture_hash_permission_and_selected_group() -> None:
    fixtures = Path(__file__).parent / "fixtures"
    xml = decode_build_code(
        (fixtures / "monk-whirling-assault-contributed.pobcode").read_text()
    )
    metadata = json.loads(
        (fixtures / "monk-whirling-assault-contributed.provenance.json").read_text()
    )
    assert hashlib.sha256(xml.encode()).hexdigest() == metadata["xml_sha256"]
    root = ElementTree.fromstring(xml)
    build = root.find("Build")
    assert build is not None and build.get("mainSocketGroup") == "8"
    groups = root.findall("Skills/SkillSet/Skill")
    main_gem = groups[7].find("Gem")
    assert main_gem is not None and main_gem.get("skillId") == "WhirlingAssaultPlayer"
    assert root.find("Notes") is None and root.find("Import") is None
    assert "Unique ID:" not in xml
    assert metadata["benchmark_eligible"] is False
    assert "User authorized" in metadata["permission"]
