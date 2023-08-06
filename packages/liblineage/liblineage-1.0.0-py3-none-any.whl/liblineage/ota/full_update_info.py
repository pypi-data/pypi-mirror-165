#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from datetime import datetime
import requests
from typing import Dict

from liblineage.constants.infra import DOMAIN
from liblineage.constants.versions import LINEAGEOS_TO_ANDROID_VERSION

API_VERSION = "v1"
API_URL = f"https://download.{DOMAIN}/api/{API_VERSION}"

class FullUpdateInfo:
	"""LineageOS full update information.

	Attributes:
	- datetime (datetime): The date and time of the update
	- filename (str): The filename of the update
	- id (str): The ID of the update
	- romtype (str): The ROM type of the update
	- size (int): The size of the update (bytes)
	- url (str): The URL of the update
	- version (str): The LineageOS version of the update (e.g. 18.1)
	"""
	def __init__(self,
		         datetime: datetime,
		         filename: str,
				 id: str,
				 romtype: str,
				 size: int,
				 url: str,
				 version: str,
		        ):
		"""Initialize the full update information."""
		self.datetime = datetime
		self.filename = filename
		self.id = id
		self.romtype = romtype
		self.size = size
		self.url = url
		self.version = version

		self.android_version = LINEAGEOS_TO_ANDROID_VERSION[version]

	@classmethod
	def from_json(self, update: Dict):
		"""Create a full update information object from a JSON object."""
		return self(datetime.fromtimestamp(update["datetime"]), update["filename"],
		            update["id"], update["romtype"],
		            update["size"], update["url"], update["version"])

	@classmethod
	def get_nightlies(cls, device: str):
		"""Get the latest OTAs for a device."""
		url = f"{API_URL}/{device}/nightly/1"
		response = requests.get(url=url).json()["response"]
		updates = [cls.from_json(update) for update in response]

		return updates
