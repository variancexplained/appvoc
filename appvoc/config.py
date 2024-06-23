#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/config.py                                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday August 21st 2023 06:36:59 pm                                                 #
# Modified   : Sunday August 27th 2023 01:45:51 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Configuration File Classes."""
from abc import ABC, abstractmethod
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# ------------------------------------------------------------------------------------------------ #
load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class Config(ABC):
    def __init__(self) -> None:
        self._mode = os.getenv("MODE")

    @property
    def mode(self) -> str:
        return self._mode

    @abstractmethod
    def get_config(self, key: str) -> str:
        """Returns the configuration for the given key

        Args:
            key (str): Key in the configuration.
        """


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
    logging: str = os.path.abspath(
        os.path.join(os.getcwd(), "../../../config/logging_jbook.yml")
    )
    web: str = os.path.abspath(os.path.join(os.getcwd(), "../../../config/web.yml"))
    persistence: str = os.path.abspath(
        os.path.join(os.getcwd(), "../../../config/persistence.yml")
    )
