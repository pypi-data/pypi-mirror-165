# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
Utils function to help on the Variscite SD card writer tool.
"""

import gzip
import io
import math
import os
import sys
from typing import List, Tuple

try:
    import yaml
except ImportError:
    sys.exit("Unable to import package 'yaml'. Please read the documentation")

from writer.config import CACHEDIR
from writer.config import MX8_YAML_CHANGELOG_FILES_B2QT
from writer.config import MX8_YAML_CHANGELOG_FILES_DEBIAN
from writer.config import MX8_YAML_CHANGELOG_FILES_YOCTO
from writer.config import SIZE_NAME
from writer.config import SOFTWARE, OS_B2QT, OS_DEBIAN
from writer.config import VAR_MODULES

from writer.ftp import connect_ftp
from writer.ftp import retrieve_remote_file


def _remote_changelog_path_b2qt(module) -> str:
    """
    Returns the remote FTP path for the B2Qt releases.
    """
    return os.path.join(module, SOFTWARE,
                        OS_B2QT, MX8_YAML_CHANGELOG_FILES_B2QT[module])

def _remote_changelog_path_debian(module) -> str:
    """
    Returns the remote FTP path for the Debian releases.
    """
    return os.path.join(module, SOFTWARE,
                        OS_DEBIAN, MX8_YAML_CHANGELOG_FILES_DEBIAN[module])

def _remote_changelog_path_yocto(module) -> str:
    """
    Returns the remote FTP path for the Yocto releases.
    """
    return os.path.join(module, SOFTWARE,
                        MX8_YAML_CHANGELOG_FILES_YOCTO[module])

def get_readable_size(size_bytes) -> str:
    """
    Returns the file size in a readable format.
    """
    if size_bytes == 0:
        return "0B"
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    size = f"{s}{SIZE_NAME[i]}"
    return size

def get_images_list_from_ftp(module_name) -> Tuple:
    """
    Returns a list of the available images from the FTP.
    """
    images = []
    module = VAR_MODULES[module_name]
    paths = _remote_changelog_path_yocto(module)
    if not (ftp_r := connect_ftp(ftp_user_name="customerv", ftp_passwd="Variscite1")):
        sys.exit("[INFO]: Could not establish FTP connection using the credentials.")

    file_path, file_name = os.path.split(paths)
    local_file = os.path.join(CACHEDIR, file_name)

    if os.path.exists(local_file):
        os.remove(local_file)

    with open(local_file, 'wb') as f:
        retrieved = retrieve_remote_file(ftp_r[0], file_name, file_path, f.write)

    if retrieved:
        yaml_file_read = read_yaml_file(local_file)
        for release in yaml_file_read:
            images.append(release)

        return images
    else:
        return None

def read_yaml_file(file_path) -> List:
    """
    Returns the YAML file content.
    """
    with open(file_path, "r") as fp:
        return list(yaml.safe_load_all(fp))


def get_file_size(yaml_file_size) -> int:
    """
    Returns image size in bytes from size in YAML file
    """
    file_size = yaml_file_size

    start = file_size.find('(') + 1
    end = file_size.find(')')

    file_size = file_size[start:end]
    file_size = int(file_size.split()[0].replace(',',''))

    return file_size

def get_gzipped_file_size(file_path) -> int:
    """
    Returns the file size.
    """
    with gzip.open(file_path, 'rb') as f:
        file_size = f.seek(0, io.SEEK_END)
    return file_size

def is_gzipped(file_path) -> bool:
    """
    Returns if file is gzipped.
    """
    with gzip.open(file_path, 'rb') as f:
        try:
            f.read(1)
            return True
        except gzip.BadGzipFile:
            return False
