#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/infrastructure/cloud/config.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday August 27th 2023 01:14:57 am                                                 #
# Modified   : Sunday August 27th 2023 04:23:39 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from dotenv import load_dotenv
import logging

from appstore.config import Config
from appstore.infrastructure.file.io import IOService

# ------------------------------------------------------------------------------------------------ #
load_dotenv()
# ------------------------------------------------------------------------------------------------ #


class CloudConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self._config_file = os.getenv("PERSISTENCE_CONFIG")
        self._config = IOService.read(self._config_file)["cloud"]
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def bucket(self) -> str:
        return self._config["aws_bucket"][self.mode]

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
