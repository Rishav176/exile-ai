"""Curate a permissioned PoB fixture without changing calculation inputs."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree

from exileai.pob.codec import decode_build_code, encode_build_xml


def anonymize_xml(xml: str) -> str:
    root = ElementTree.fromstring(xml)
    for parent in root.iter():
        if parent.tag == "Item" and parent.text:
            parent.text = re.sub(
                r"(?m)^[ \t]*Unique ID:[^\n]*(?:\n|$)", "", parent.text
            )
        for child in list(parent):
            if child.tag in {"Notes", "Import", "Note"}:
                parent.remove(child)
        for key in list(parent.attrib):
            if key.lower() in {
                "accountname",
                "charactername",
                "buildname",
                "importlink",
                "lastcharacterhash",
                "lastrealm",
                "itempburl",
                "label",
                "title",
            }:
                del parent.attrib[key]
    return ElementTree.tostring(root, encoding="unicode", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("code", type=Path)
    args = parser.parse_args()
    xml = decode_build_code(args.code.read_text())
    sanitized = anonymize_xml(xml)
    print(
        json.dumps(
            {
                "code": encode_build_xml(sanitized),
                "xml_sha256": hashlib.sha256(sanitized.encode()).hexdigest(),
                "original_xml_sha256": hashlib.sha256(xml.encode()).hexdigest(),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
