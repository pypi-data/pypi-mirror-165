#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from typing import Dict, List

from urllib.parse import urlparse


class Base:
    def url_validation(self, url):
        urlScheme = urlparse(url)
        if urlScheme.scheme not in ["http", "https"]:
            raise TypeError("Invalid url input.")

    def url_path(self):
        return urlparse(self.url)


@dataclass
class YamlValidator(Base):

    url: str
    squad_group: str
    branches: List[Dict]

    def __post_init__(self):
        self.url_validation(self.url)
