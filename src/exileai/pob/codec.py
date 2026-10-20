"""PoB2's URL-safe Base64 and zlib/gzip transport, independent of calculations."""

import base64
import binascii
import zlib
from xml.etree import ElementTree


class InvalidBuildCode(ValueError):
    """The input is not a bounded PoB2 XML share code."""


def encode_build_xml(xml: str) -> str:
    return base64.urlsafe_b64encode(zlib.compress(xml.encode())).decode()


def decode_build_code(code: str, *, max_xml_bytes: int = 4_000_000) -> str:
    if len(code) > 8_000_000 or max_xml_bytes < 1:
        raise InvalidBuildCode("Build code exceeds input limits")
    normalized = "".join(code.split())
    if not normalized:
        raise InvalidBuildCode("Build code is empty")
    try:
        compressed = base64.b64decode(
            normalized + "=" * (-len(normalized) % 4), altchars=b"-_", validate=True
        )
        stream = zlib.decompressobj(zlib.MAX_WBITS | 32)
        data = stream.decompress(compressed, max_xml_bytes + 1)
        if len(data) > max_xml_bytes or not stream.eof or stream.unused_data:
            raise InvalidBuildCode("Invalid or oversized compressed build")
        xml = data.decode("utf-8")
        if "<!DOCTYPE" in xml.upper() or "<!ENTITY" in xml.upper():
            raise InvalidBuildCode("XML declarations with entities are unsupported")
        if ElementTree.fromstring(xml).tag != "PathOfBuilding2":
            raise InvalidBuildCode("Expected a PathOfBuilding2 XML document")
        return xml
    except (binascii.Error, zlib.error, UnicodeError, ElementTree.ParseError) as error:
        raise InvalidBuildCode("Invalid PoB2 build code") from error
