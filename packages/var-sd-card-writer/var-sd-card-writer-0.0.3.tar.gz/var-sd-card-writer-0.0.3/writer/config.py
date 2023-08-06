# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
Configuration file for the SD card writer tool.
"""

import os

BLOCK_SIZE = 1024
CHUNK = BLOCK_SIZE * BLOCK_SIZE

VAR_SD_CARD_WRITER_FOLDER = "varwriter"
CACHEDIR = os.path.join(os.environ['HOME'], ".cache", VAR_SD_CARD_WRITER_FOLDER)

SIZE_NAME = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

IGNORED_DEVICE_PATHS = {'/dm', '/loop', '/md'}

SOFTWARE = "Software"
OS_YOCTO = "yocto"
OS_DEBIAN = "debian"
OS_B2QT = "b2qt"

FTP_DOMAIN_HOST_NAME = "ftp.variscite.com"
FTP_PASSWD_READ_ONLY = "customerv"
FTP_USER_NAME_READ_ONLY = "Variscite1"

YAML_CHANGELOG_MX8M_B2QT    = "mx8m-b2qt-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8M_DEBIAN  = "mx8m-debian-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8M_YOCTO   = "mx8m-recovery-sd-changelog.yml"

YAML_CHANGELOG_MX8MM_B2QT   = "mx8mm-b2qt-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8MM_DEBIAN = "mx8mm-debian-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8MM_YOCTO  = "mx8mm-recovery-sd-changelog.yml"

YAML_CHANGELOG_MX8MP_B2QT   = "mx8mp-b2qt-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8MP_DEBIAN = "mx8mp-debian-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8MP_YOCTO  = "mx8mp-recovery-sd-changelog.yml"

YAML_CHANGELOG_MX8_B2QT     = "mx8-b2qt-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8_DEBIAN   = "mx8-debian-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8_YOCTO    = "mx8-recovery-sd-changelog.yml"

YAML_CHANGELOG_MX8X_B2QT    = "mx8x-b2qt-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8X_DEBIAN  = "mx8x-debian-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8X_YOCTO   = "mx8x-recovery-sd-changelog.yml"

YAML_CHANGELOG_MX8MN_B2QT   = "mx8mn-b2qt-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8MN_DEBIAN = "mx8mn-debian-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8MN_YOCTO  = "mx8mn-recovery-sd-changelog.yml"

MX8M    = "DART-MX8M"
MX8MM   = "DART-MX8M-MINI"
MX8MP   = "DART-MX8M-PLUS"

MX8     = "VAR-SOM-MX8"
MX8X    = "VAR-SOM-MX8X"
MX8MN   = "VAR-SOM-MX8M-NANO"

MX8_YAML_CHANGELOG_FILES_B2QT = {
         MX8M  : YAML_CHANGELOG_MX8M_B2QT,
         MX8MM : YAML_CHANGELOG_MX8MM_B2QT,
         MX8MP : YAML_CHANGELOG_MX8MP_B2QT,
         MX8   : YAML_CHANGELOG_MX8_B2QT,
         MX8X  : YAML_CHANGELOG_MX8X_B2QT,
         MX8MN : YAML_CHANGELOG_MX8MN_B2QT}

MX8_YAML_CHANGELOG_FILES_DEBIAN = {
         MX8M  : YAML_CHANGELOG_MX8M_DEBIAN,
         MX8MM : YAML_CHANGELOG_MX8MM_DEBIAN,
         MX8MP : YAML_CHANGELOG_MX8MP_DEBIAN,
         MX8   : YAML_CHANGELOG_MX8_DEBIAN,
         MX8X  : YAML_CHANGELOG_MX8X_DEBIAN,
         MX8MN : YAML_CHANGELOG_MX8MN_DEBIAN}

MX8_YAML_CHANGELOG_FILES_YOCTO = {
         MX8M  : YAML_CHANGELOG_MX8M_YOCTO,
         MX8MM : YAML_CHANGELOG_MX8MM_YOCTO,
         MX8MP : YAML_CHANGELOG_MX8MP_YOCTO,
         MX8   : YAML_CHANGELOG_MX8_YOCTO,
         MX8X  : YAML_CHANGELOG_MX8X_YOCTO,
         MX8MN : YAML_CHANGELOG_MX8MN_YOCTO}

VAR_MODULES = {
        "MX8"    : MX8,
        "MX8X"   : MX8X,
        "MX8M"   : MX8M,
        "MX8MN"  : MX8MN,
        "MX8MM"  : MX8MM,
        "MX8MP"  : MX8MP}
