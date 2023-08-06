"""Implementation of the Compact Muon Solenoid (CMS) file catalog lookup (storage.xml) """
from __future__ import annotations

import re
from dataclasses import field
from xml.dom.minidom import parse as parse_xml

from ._base import StorageCatalog


class CMSStorageCatalog(StorageCatalog):
    """CMS file catalog lookup"""

    config: str = "storage.xml"
    protocol: str = "direct"
    transformation_rules: list[tuple[re.Pattern[str], str]] = field(
        default_factory=list
    )

    def __init__(self, config: str | None = None, protocol: str | None = None) -> None:
        if config is not None:
            self.config = config
        if protocol is not None:
            self.protocol = protocol
        self.transformation_rules = self.__read_config()

    def __read_config(self) -> list[tuple[re.Pattern[str], str]]:
        """Reads the CMS storage catalog"""

        cms_rules: list[tuple[re.Pattern[str], str]] = []
        with parse_xml(self.config) as dom:
            rules = dom.getElementsByTagName("lfn-to-pfn")
            for rule in rules:
                if rule.getAttribute("protocol") != self.protocol:
                    continue
                pattern = re.compile(rule.getAttribute("path-match"))
                result = rule.getAttribute("result")
                cms_rules.append((pattern, result))
        return cms_rules

    def is_cms_path(self, path: str) -> bool:
        """Checks if the path is a CMS path"""
        cms_regex = re.compile(r"^/*(store.*)")
        match = cms_regex.match(path)
        if match:
            return True
        return False

    def lfn2pfn(self, lfn: str) -> str:
        """Converts logical filename to physical filename"""
        for rule in self.transformation_rules:
            pattern, result = rule
            match = pattern.match(lfn)
            if match is None:
                continue
            result = result.replace("$", "\\")
            return match.expand(result)
        return lfn
