#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/scraper/appstore/config/selector.py                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:11:49 am                                                 #
# Modified   : Saturday April 8th 2023 02:59:16 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from dotenv import load_dotenv
import logging

from aimobile.service.scraper.appstore import exceptions


# ------------------------------------------------------------------------------------------------ #
class Config:
    __config_filepaths = {
        "prod": "aimobile/service/scraper/appstore/config/config_prod.yml",
        "dev": "aimobile/service/scraper/appstore/config/config_dev.yml",
        "test": "aimobile/service/scraper/appstore/config/config_test.yml",
    }

    @classmethod
    @property
    def file(cls) -> str:
        """Returns the config filepath for the current mode in ['dev','test','prod']"""
        logger = logging.getLogger(f"{cls.__module__}.{cls.__class__.__name__}")
        load_dotenv()
        mode = os.getenv("MODE", default="test")
        try:
            return cls.__config_filepaths[mode]
        except KeyError:
            msg = f"Mode={mode} is invalid. Must be in ['prod','dev','test']. Check environment variable."
            logger.error(msg)
            raise exceptions.InvalidMode(msg)
