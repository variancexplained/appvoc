#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/infrastructure/database/config.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday August 27th 2023 01:14:57 am                                                 #
# Modified   : Sunday August 27th 2023 02:13:21 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from dotenv import load_dotenv
import logging

from appvoc.config import Config
from appvoc.infrastructure.file.io import IOService

# ------------------------------------------------------------------------------------------------ #
load_dotenv()
# ------------------------------------------------------------------------------------------------ #


class DatabaseConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self._config_file = os.getenv("PERSISTENCE_CONFIG")
        self._config = IOService.read(self._config_file)["database"]
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def name(self) -> str:
        return self._config["name"][self.mode]

    @property
    def backup_directory(self) -> str:
        return self._config["backup"][self.mode]

    @property
    def username(self) -> str:
        return os.getenv("MYSQL_USERNAME")

    @property
    def password(self) -> str:
        return os.getenv("MYSQL_PWD")

    @property
    def startup(self) -> str:
        return os.getenv("MYSQL_STARTUP_SCRIPT")

    def get_config(self, key: str) -> str:
        """Returns the configuration for the given key

        Args:
            key (str): Key in the configuration.
        """
        if key not in self._config.keys():
            msg = f"Key {key} is not in the cloud configuration."
            self._logger.info(msg)
            return None
        else:
            return self._config[key][self.mode]
