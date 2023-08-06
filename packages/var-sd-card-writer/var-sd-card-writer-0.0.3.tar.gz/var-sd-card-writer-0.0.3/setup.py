# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import os
from setuptools import setup, find_packages
import re
import sys

import requests

from writer import __version__

VAR_EXTERNAL_WRITER = os.path.join(os.getcwd(), "writer", "writer.py")
WRITER_USR = os.path.join(os.environ['HOME'], ".local", "bin", "external_writer_var")

if os.path.exists(WRITER_USR):
    os.system("rm -rf {}".format(WRITER_USR))

os.system("cp {} {}".format(VAR_EXTERNAL_WRITER, WRITER_USR))

VAR_SD_CARD_WRITER_FOLDER = "varwriter"
CACHEDIR = os.path.join(os.environ['HOME'], ".cache", VAR_SD_CARD_WRITER_FOLDER)

VAR_SD_CARD_WRITER_ASSETS = "assets"
CACHEDIR_ASSETS = os.path.join(CACHEDIR, VAR_SD_CARD_WRITER_ASSETS)

ASSETS_CSS_NAME = "writer.css"
ASSETS_LOGO_NAME = "variscite.png"
ASSETS_ICON_NAME = "variscite_icon.png"

url_css = "https://github.com/varigit/var-sd-card-writer/raw/master/writer/assets/writer.css"
url_logo = "https://github.com/varigit/var-sd-card-writer/raw/master/writer/assets/variscite.png"
url_icon = "https://github.com/varigit/var-sd-card-writer/raw/master/writer/assets/variscite_icon.png"

try:
    os.mkdir(CACHEDIR)
except:
    pass

try:
    os.mkdir(CACHEDIR_ASSETS)
except:
    pass

r = requests.get(url_css, allow_redirects=True)
open(f"{CACHEDIR_ASSETS}/{ASSETS_CSS_NAME}", 'wb').write(r.content)

r = requests.get(url_logo, allow_redirects=True)
open(f"{CACHEDIR_ASSETS}/{ASSETS_LOGO_NAME}", 'wb').write(r.content)

r = requests.get(url_icon, allow_redirects=True)
open(f"{CACHEDIR_ASSETS}/{ASSETS_ICON_NAME}", 'wb').write(r.content)

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "var-sd-card-writer",
    version = __version__,
    author = "Alifer Moraes, Diego Dorta",
    description = "Variscite SD Card Writer Tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = "BSD-3-Clause",
    url = "https://github.com/varigit/var-sd-card-writer",
    packages=find_packages(),
    entry_points = {
        'console_scripts' : ['var-sd-card-writer = writer.varwriter:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 3.7'
    ],
)
