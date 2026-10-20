import base64
import gzip
import zlib

import pytest

from exileai.pob.codec import InvalidBuildCode, decode_build_code, encode_build_xml

XML = '<PathOfBuilding2><Build targetVersion="0_1"/></PathOfBuilding2>'


def test_round_trip_and_unpadded_input() -> None:
    assert decode_build_code(encode_build_xml(XML).rstrip("=")) == XML


def test_accepts_gzip_transport() -> None:
    code = base64.urlsafe_b64encode(gzip.compress(XML.encode())).decode()
    assert decode_build_code(code) == XML


@pytest.mark.parametrize("value", ["", "https://example.com/build", "invalid!", "eA=="])
def test_invalid_codes_fail_explicitly(value: str) -> None:
    with pytest.raises(InvalidBuildCode):
        decode_build_code(value)


def test_rejects_non_pob2_and_xml_entities() -> None:
    for xml in (
        "<PathOfBuilding/>",
        '<!DOCTYPE x [<!ENTITY a "test">]><PathOfBuilding2/>',
    ):
        with pytest.raises(InvalidBuildCode):
            decode_build_code(encode_build_xml(xml))


def test_rejects_bounded_decompression_and_trailing_streams() -> None:
    with pytest.raises(InvalidBuildCode):
        decode_build_code(encode_build_xml(XML), max_xml_bytes=10)
    code = base64.urlsafe_b64encode(zlib.compress(XML.encode()) + b"junk").decode()
    with pytest.raises(InvalidBuildCode):
        decode_build_code(code)
