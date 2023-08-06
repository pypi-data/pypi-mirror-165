#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Alexander Pace, Tanner Presetegard, Branson Stephens (2019)
#
# This file is part of lvalert-overseer
#
# lvalert-overseer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lvalert-overseer.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages

version = "0.5.2"
AUTHOR = 'Alexander Pace'
AUTHOR_EMAIL = 'alexander.pace@ligo.org'
LICENSE = 'GPLv3'

description = "igwn-alert Overseer Server and Client Tools"
long_description = """The igwn-alert overseer provides a way to maintain an open
connection to igwn-alert for sending message, and to log the outgoing and
incoming messages and measure latencies."""

setup(
    name="igwn-alert-overseer",
    version=version,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=description,
    long_description=long_description,
    url=None,
    license=LICENSE,
    namespace_packages=['igwn_alert_overseer'],
    packages=find_packages(),
    scripts=['bin/igwn_alert_overseer', 'bin/overseer_test_client'],
    install_requires=['twisted',
                      'igwn-alert>=0.2.2'],
)
