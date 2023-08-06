#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

import requests

from liblineage.constants.infra import GITHUB_ORG

LINEAGE_BUILD_TARGETS_FILE = f"https://raw.githubusercontent.com/{GITHUB_ORG}/hudson/master/lineage-build-targets"

class BuildTarget:
	def __init__(self,
	             device: str,
	             build_type: str,
	             branch_name: str,
	             period: str,
	            ):
		self.device = device
		self.build_type = build_type
		self.branch_name = branch_name
		self.period = period

	def __str__(self) -> str:
		return f"{self.device} {self.build_type} {self.branch_name} {self.period}"

	@classmethod
	def from_api(cls, line: str):
		return cls(*line.split())

	@classmethod
	def get_lineage_build_targets(cls):
		response = requests.get(url=LINEAGE_BUILD_TARGETS_FILE).text.split("\n")
		return [cls.from_api(line) for line in response if line and not line.startswith("#")]
