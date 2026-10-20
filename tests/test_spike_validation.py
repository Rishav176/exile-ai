from pathlib import Path

import pytest

from exileai.pob.codec import decode_build_code
from exileai.pob.validation import (
    UnsupportedBuild,
    validate_spike_scenario,
    validate_spike_xml,
)


def fixture_xml() -> str:
    return decode_build_code(
        (Path(__file__).parent / "fixtures/spark-diagnostic.pobcode").read_text()
    )


def test_accepts_exact_fixture_allocation() -> None:
    assert validate_spike_xml(fixture_xml()) == [4739, 54447]


@pytest.mark.parametrize(
    "old,new",
    [
        ('treeVersion="0_5"', 'treeVersion="0_4"'),
        ('targetVersion="0_1"', 'targetVersion="old"'),
        ('nodes="4739,54447"', 'nodes="4739,4739"'),
    ],
)
def test_rejects_conversion_or_invalid_allocations(old: str, new: str) -> None:
    with pytest.raises(UnsupportedBuild):
        validate_spike_xml(fixture_xml().replace(old, new))


def test_rejects_unverified_buff_override() -> None:
    xml = fixture_xml().replace(
        '<ConfigSet id="1">',
        '<ConfigSet id="1"><Input name="usePowerCharges" boolean="true"/>',
    )
    with pytest.raises(UnsupportedBuild, match="needs audit"):
        validate_spike_xml(xml)


@pytest.mark.parametrize(
    "element",
    [
        '<Input name="customMods" string="100% more Damage"/>',
        '<Placeholder name="usePowerCharges" string="true"/>',
    ],
)
def test_rejects_legacy_and_placeholder_input_bypasses(element: str) -> None:
    xml = fixture_xml().replace(
        '<Config activeConfigSet="1">', '<Config activeConfigSet="1">' + element
    )
    with pytest.raises(UnsupportedBuild, match="needs audit"):
        validate_spike_xml(xml)


@pytest.mark.parametrize(
    "config",
    [
        {},
        {"enemyIsBoss": "None", "enemyLevel": 82, "enemyDamageType": "Average"},
        {
            "enemyIsBoss": "Pinnacle",
            "enemyLevel": 82,
            "enemyDamageType": "Average",
            "usePowerCharges": True,
        },
    ],
)
def test_rejects_mislabeled_benchmark_settings(config: dict[str, object]) -> None:
    with pytest.raises(UnsupportedBuild, match="scenario configuration"):
        validate_spike_scenario({"id": "solo-sustained-pinnacle-v1", "config": config})
