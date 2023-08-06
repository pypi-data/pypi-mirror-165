#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from typing import Dict, Union

from liblineage.wiki.data_types.base_data import BaseData

class SdcardData(BaseData):
	"""The format required for the sdcard property.

	Attributes:
	- sizeMax: Maximum size for a sdcard
	- slot: where the sdcard is inserted
	"""
	def __init__(self,
	             sizeMax: str,
	             slot: str = None
	            ):
		"""Initialize the sdcard information."""
		super().__init__()

		self.sizeMax = sizeMax
		self.slot = slot

	@classmethod
	def from_data(cls, data: Union[None, Dict]) -> Union[None, "SdcardData"]:
		"""Create a sdcard information object from YAML data."""
		if data is None:
			sdcard = None
		elif isinstance(data, dict):
			sdcard = cls.from_dict(data)
		else:
			raise Exception("Invalid sdcard data")

		return sdcard
