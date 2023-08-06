#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from datetime import date
import requests
from typing import Dict, List, Union
import yaml

from liblineage.constants.infra import GITHUB_ORG, GITHUB_ORG_URL
from liblineage.wiki.data_types.architecture_data import ArchitectureData
from liblineage.wiki.data_types.battery_data import BatteryData
from liblineage.wiki.data_types.bluetooth_data import BluetoothData
from liblineage.wiki.data_types.camera_data import CameraData
from liblineage.wiki.data_types.dimension_data import DimensionData
from liblineage.wiki.data_types.peripherals_data import PeripheralsData
from liblineage.wiki.data_types.release_data import ReleaseData
from liblineage.wiki.data_types.screen_data import ScreenData
from liblineage.wiki.data_types.sdcard_data import SdcardData

class DeviceData:
	"""LineageOS wiki device data.

	Attributes:
	- architecture: The architecture of the device
	- battery: Battery info
	- bluetooth: Bluetooth support info
	- codename: The codename of the device
	- cpu: CPU name
	- cpu_cores: Number of CPU cores
	- cpu_freq: CPU frequency
	- current_branch: The current branch of the device
	- dimensions: Dimensions of the device
	- gpu: GPU name
	- image: The image of the device
	- install_method: The install method of the device
	- kernel: Kernel repository
	- maintainers: The maintainers of the device
	- name: Commercial name of the device
	- peripherals: Peripherals supported by the device
	- release: The release date of the device
	- screen: Screen info
	- tree: Device tree repository of the device
	- type: The form factor of the device
	- vendor: Brand name of the device vendor
	- vendor_short: Short name of the device vendor
	- versions: The versions of the device

	Optional attributes:
	- before_install: The before_install script for the device
	- before_lineage_install: The before_lineage_install script for the device
	- before_recovery_install: The before_recovery_install script for the device
	- cameras: The cameras of the device
	- carrier: The carrier of the device
	- custom_recovery_codename: The custom recovery codename of the device
	- custom_recovery_link: The custom recovery link of the device
	- custom_unlock_cmd: The custom unlock command of the device
	- download_boot: The download boot of the device
	- format_on_upgrade: Whether to format on upgrade
	- has_recovery_partition: Whether the device has a recovery partition
	- is_ab_device: Whether the device is an A/B device
	- is_unlockable: Whether the device is unlockable
	- models: The models of the device
	- network: The network of the device
	- recovery_boot: The recovery boot of the device
	- required_bootloader: The required bootloader of the device
	- sdcard: The SD card info of the device
	- uses_twrp: Whether the device uses TWRP
	"""
	def __init__(self,
	             architecture: Union[str, ArchitectureData],
	             battery: Union[BatteryData, Dict[str, BatteryData], None],
	             bluetooth: Union[BluetoothData, None],
	             codename: str,
	             cpu: str,
	             cpu_cores: Union[int, str],
	             cpu_freq: str,
	             current_branch: float,
	             dimensions: Union[DimensionData, Dict[str, DimensionData], None],
	             gpu: str,
	             image: str,
	             install_method: str,
	             kernel: str,
	             maintainers: List[str],
	             name: str,
	             peripherals: Union[List[str], Dict[str, List[str]], None],
	             release: Union[date, Dict[str, date]],
	             screen: Union[ScreenData, Dict[str, ScreenData], None],
	             tree: str,
	             type: str,
	             vendor: str,
	             vendor_short: str,
	             versions: List[float],

				 before_install: Union[str, None] = None,
				 before_lineage_install: Union[str, None] = None,
				 before_recovery_install: Union[str, None] = None,
				 cameras: Union[List[CameraData], None] = None,
				 carrier: Union[str, None] = None,
				 custom_recovery_codename: Union[str, None] = None,
				 custom_recovery_link: Union[str, None] = None,
				 custom_unlock_cmd: Union[str, None] = None,
				 download_boot: Union[str, None] = None,
				 format_on_upgrade: Union[bool, None] = None,
				 has_recovery_partition: Union[bool, None] = None,
				 is_ab_device: Union[bool, None] = None,
				 is_unlockable: Union[bool, None] = None,
				 models: Union[List[str], None] = None,
				 network: Union[List[str], None] = None,
				 recovery_boot: Union[str, None] = None,
				 required_bootloader: Union[List[str], None] = None,
				 sdcard: Union[SdcardData, None] = None,
				 uses_twrp: Union[bool, None] = None,
	            ):
		"""Initialize the device information."""
		self.architecture = architecture
		self.battery = battery
		self.bluetooth = bluetooth
		self.codename = codename
		self.cpu = cpu
		self.cpu_cores = cpu_cores
		self.cpu_freq = cpu_freq
		self.current_branch = current_branch
		self.dimensions = dimensions
		self.gpu = gpu
		self.image = image
		self.install_method = install_method
		self.kernel = kernel
		self.maintainers = maintainers
		self.name = name
		self.peripherals = peripherals
		self.release = release
		self.screen = screen
		self.tree = tree
		self.type = type
		self.vendor = vendor
		self.vendor_short = vendor_short
		self.versions = versions

		self.before_install = before_install
		self.before_lineage_install = before_lineage_install
		self.before_recovery_install = before_recovery_install
		self.cameras = cameras
		self.carrier = carrier
		self.custom_recovery_codename = custom_recovery_codename
		self.custom_recovery_link = custom_recovery_link
		self.custom_unlock_cmd = custom_unlock_cmd
		self.download_boot = download_boot
		self.format_on_upgrade = format_on_upgrade
		self.has_recovery_partition = has_recovery_partition
		self.is_ab_device = is_ab_device
		self.is_unlockable = is_unlockable
		self.models = models
		self.network = network
		self.recovery_boot = recovery_boot
		self.required_bootloader = required_bootloader
		self.sdcard = sdcard
		self.uses_twrp = uses_twrp

	@classmethod
	def from_dict(cls, data: Dict):
		"""Create a device data object from a dictionary."""
		return cls(
			architecture = ArchitectureData.from_data(data["architecture"]),
			battery = BatteryData.from_data(data["battery"]),
			bluetooth = BluetoothData.from_data(data["bluetooth"]),
			codename = data["codename"],
			cpu = data["cpu"],
			cpu_cores = data["cpu_cores"],
			cpu_freq = data["cpu_freq"],
			current_branch = data["current_branch"],
			dimensions = DimensionData.from_data(data["dimensions"]),
			gpu = data["gpu"],
			image = data["image"],
			install_method = data["install_method"],
			kernel = data["kernel"],
			maintainers = data["maintainers"],
			name = data["name"],
			peripherals = PeripheralsData.from_data(data["peripherals"]),
			release = ReleaseData.from_data(data["release"]),
			screen = ScreenData.from_data(data["screen"]),
			tree = data["tree"],
			type = data["type"],
			vendor = data["vendor"],
			vendor_short = data["vendor_short"],
			versions = data["versions"],

			before_install = data.get("before_install"),
			before_lineage_install = data.get("before_lineage_install"),
			before_recovery_install = data.get("before_recovery_install"),
			cameras = CameraData.from_data(data.get("cameras")),
			carrier = data.get("carrier"),
			custom_recovery_codename = data.get("custom_recovery_codename"),
			custom_recovery_link = data.get("custom_recovery_link"),
			custom_unlock_cmd = data.get("custom_unlock_cmd"),
			download_boot = data.get("download_boot"),
			format_on_upgrade = data.get("format_on_upgrade"),
			has_recovery_partition = data.get("has_recovery_partition"),
			is_ab_device = data.get("is_ab_device"),
			is_unlockable = data.get("is_unlockable"),
			models = data.get("models"),
			network = data.get("network"),
			recovery_boot = data.get("recovery_boot"),
			required_bootloader = data.get("required_bootloader"),
			sdcard = SdcardData.from_data(data.get("sdcard")),
			uses_twrp = data.get("uses_twrp"),
		)

	@classmethod
	def get_device_data(cls, device: str):
		url = f"https://raw.githubusercontent.com/{GITHUB_ORG}/lineage_wiki/master/_data/devices/{device}.yml"
		response = requests.get(url=url)
		response.raise_for_status()
		return cls.from_dict(yaml.safe_load(response.text))

	def __str__(self) -> str:
		"""Return a string representation of the device data."""
		infos = {
			"Name": self.name,
			"Codename": self.codename,
			"Architecture": self.architecture,
			"Battery": ", ".join([f'{device}: {battery_data}' for device, battery_data in self.battery.items()]) if isinstance(self.battery, dict) else self.battery,
			"Bluetooth": self.bluetooth,
			"CPU": self.cpu,
			"CPU cores": self.cpu_cores,
			"CPU frequency": self.cpu_freq,
			"Dimensions": ", ".join([f'{device}: {dimensions_data}' for device, dimensions_data in self.dimensions.items()]) if isinstance(self.dimensions, dict) else self.dimensions,
			"GPU": self.gpu,
			"Kernel repository": f"{GITHUB_ORG_URL}/{self.kernel}",
			"Maintainers": ", ".join(self.maintainers) if self.maintainers else "None (unmaintained)",
			"Peripherals": ", ".join(self.peripherals) if isinstance(self.peripherals, list) else ", ".join([f'{device}: {", ".join(peripherals)}' for device, peripherals in self.peripherals.items()]) if isinstance(self.peripherals, dict) else self.peripherals,
			"Release": ", ".join([f'{device}: {date}' for device, date in self.release.items()]) if isinstance(self.release, dict) else self.release,
			"Screen": ", ".join([f'{device}: {screen_data}' for device, screen_data in self.screen.items()]) if isinstance(self.screen, dict) else self.screen,
			"Device tree repository": f'{GITHUB_ORG_URL}/{self.tree}',
			"Type": self.type,
			"Vendor": self.vendor,
			"Vendor (short)": self.vendor_short,
			"Versions": ", ".join([f'{version}' for version in self.versions]),
		}

		opt_infos = {
			key: value for key, value in {
				"Cameras": ", ".join([f'{camera}' for camera in self.cameras]) if isinstance(self.cameras, list) else self.cameras,
				"Carrier": self.carrier,
				"Custom recovery codename": self.custom_recovery_codename,
				"Custom recovery link": self.custom_recovery_link,
				"Custom unlock command": self.custom_unlock_cmd,
				"Download boot": self.download_boot,
				"Format on upgrade": self.format_on_upgrade,
				"Has recovery partition": self.has_recovery_partition,
				"Is A/B device": self.is_ab_device,
				"Is unlockable": self.is_unlockable,
				"Models": ", ".join(self.models) if isinstance(self.models, list) else self.models,
				"Network": ", ".join(self.network) if isinstance(self.network, list) else self.network,
				"Recovery boot": self.recovery_boot,
				"Required bootloader": self.required_bootloader,
				"SD card": self.sdcard,
				"Uses TWRP": self.uses_twrp,
			}.items()
			if value is not None
		}

		return "\n".join([f"{key}: {value}" for key, value in {
			**infos,
			**opt_infos,
		}.items()])
