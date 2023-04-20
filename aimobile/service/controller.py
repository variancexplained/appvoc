#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /service/controller.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Thursday April 20th 2023 06:56:18 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class Controller(ABC):
    """Scraper controller responsible for scraping and persisting a target or series of URLs."""

    @abstractmethod
    def scrape(self, config: dict, *args, **kwargs) -> None:
        """Accepts a config file, instantiates a scraper, controls the iteratio and persists the results.

        Args:
            config (dict): Configuration file specifying the parameters of the scraping project.
        """
