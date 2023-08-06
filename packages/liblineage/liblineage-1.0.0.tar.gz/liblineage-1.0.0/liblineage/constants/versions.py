#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from sebaubuntu_libs.libandroid.versions import AndroidVersion

LINEAGEOS_TO_ANDROID_VERSION = {}
ANDROID_TO_LINEAGEOS_VERSION = {}

for key, value in {
	"13.0": AndroidVersion.M,
	"14.1": AndroidVersion.N,
	"15.1": AndroidVersion.O,
	"16.0": AndroidVersion.P,
	"17.1": AndroidVersion.Q,
	"18.0": AndroidVersion.R,
	"18.1": AndroidVersion.R,
	"19.0": AndroidVersion.S,
	"19.1": AndroidVersion.S_V2,
	"20.0": AndroidVersion.TIRAMISU,
}.items():
	LINEAGEOS_TO_ANDROID_VERSION[key] = value
	ANDROID_TO_LINEAGEOS_VERSION[value] = key
