#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/config.py                                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday August 21st 2023 06:36:59 pm                                                 #
# Modified   : Monday August 21st 2023 07:23:58 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Configuration File Classes."""
from abc import ABC
import os
from dataclasses import dataclass


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ConfigFile(ABC):
    logging: str
    web: str
    persistence: str


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ConfigFileDefault(ConfigFile):
    logging: str = "config/logging.yml"
    web: str = "config/web.yml"
    persistence: str = "config/persistence.yml"


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ConfigFileJBook(ConfigFile):
    logging: str = os.path.abspath(os.path.join(os.getcwd(), "../../../config/logging_jbook.yml"))
    web: str = os.path.abspath(os.path.join(os.getcwd(), "../../../config/web.yml"))
    persistence: str = os.path.abspath(os.path.join(os.getcwd(), "../../../config/persistence.yml"))
