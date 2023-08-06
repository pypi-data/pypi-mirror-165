#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from typing import Dict, List, Union

from liblineage.wiki.data_types.base_data import BaseData

class ScreenData(BaseData):
	"""LineageOS screen information.

	Attributes:
	- size: The screen size (inches)
	- density: The screen density (dpi)
	- resolution: The screen resolution (e.g. 1080x1920)
	- technology: The screen technology (e.g. LCD)
	"""
	def __init__(self,
	             size: str,
	             density: int,
	             resolution: str,
	             technology: str,
	            ):
		"""Initialize the screen information."""
		super().__init__()

		self.size = size
		self.density = density
		self.resolution = resolution
		self.technology = technology

	@classmethod
	def from_data(cls, data: Union[None, Dict, List, str]) -> Union[None, "ScreenData", Dict[str, "ScreenData"], None]:
		"""Create a screen information object from YAML data."""
		if data is None:
			screen = None
		elif isinstance(data, dict):
			screen = cls.from_dict(data)
		elif isinstance(data, list):
			screen = {}
			for scr in data:
				device, screen_data = list(scr.items())[0]
				screen[device] = cls.from_dict(screen_data)
		elif isinstance(data, str) and data == "None":
			screen = None
		else:
			raise Exception("Invalid screen data")

		return screen
