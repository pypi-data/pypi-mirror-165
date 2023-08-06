# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
Functions to handle the FTP server from Variscite.
"""

import ftplib
import os
import sys
from typing import Tuple

from writer.config import BLOCK_SIZE
from writer.config import CACHEDIR
from writer.config import FTP_DOMAIN_HOST_NAME
from writer.config import FTP_PASSWD_READ_ONLY
from writer.config import FTP_USER_NAME_READ_ONLY


def connect_ftp(ftp_user_name=FTP_USER_NAME_READ_ONLY,
                ftp_passwd=FTP_PASSWD_READ_ONLY,
                ftp_host_name=FTP_DOMAIN_HOST_NAME,
                ftp_timeout=100) -> Tuple[str, bool]:
    """
    Creates a connection to the FTP.
    """
    try:
        ftp = ftplib.FTP(ftp_host_name, timeout=ftp_timeout)
        ftp.login(user=ftp_user_name, passwd=ftp_passwd)
    except ftplib.all_errors as error:
        sys.stderr.write(f"[FTP]: Fail to connect to {ftp_host_name}: {error}\n")
        return False, error
    return ftp, False

def retrieve_remote_file(ftp, file_name, remote_path, writer) -> bool:
    """
    Retrieves a remote file from the FTP server.
    """
    local_file = os.path.join(CACHEDIR, file_name)
    try:
        ftp.cwd(remote_path)
        res = ftp.retrbinary(f"RETR {file_name}", writer, blocksize=BLOCK_SIZE)
        if not res.startswith("226 Transfer complete"):
            os.remove(local_file)
            return False
    except ftplib.all_errors as error:
        sys.stderr.write(f"[FTP]: Fail to retrieve '{local_file}': {error}\n")
        ftp.quit()
        return False
    ftp.quit()
    return True
