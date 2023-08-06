#!/usr/bin/env python3

# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import os
from pathlib import Path
import sys

import gzip

CHUNK = 1024 * 1024

def is_gzipped(file_path):
    with gzip.open(file_path, 'rb') as f:
        try:
            f.read(1)
            return True
        except gzip.BadGzipFile:
            return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Unexpected number of arguments")

    image_path = sys.argv[1]
    image_size = int(sys.argv[2])
    device = sys.argv[3]

    if not Path(image_path).is_file():
        sys.exit(f"{image_path} is not a regular file")

    if not Path(device).is_block_device():
        sys.exit(f"{device} is not a valid block device")

    # Force stdout line buffering
    sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)

    bytes_written = 0
    dev_fd = os.open(device, os.O_WRONLY)
    with os.fdopen(dev_fd, 'wb') as dev:
        if is_gzipped(image_path):
            open = gzip.open

        with open(image_path, 'rb') as file_obj:
            data = file_obj.read(CHUNK)
            while len(data):
                dev.write(data)
                bytes_written += len(data)
                print(f"{bytes_written}/{image_size}")
                data = file_obj.read(CHUNK)
            print(f"Synching image permanently to the device. It may take a while")
        os.fsync(dev_fd)