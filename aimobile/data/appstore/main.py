#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/appstore/main.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:25:30 am                                                #
# Modified   : Tuesday April 18th 2023 11:15:14 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os

from aimobile.data.appstore import directories
from aimobile.framework.container import AppStoreContainer


# ------------------------------------------------------------------------------------------------ #
def make_directories() -> None:
    """Creates the directories required for logging and database persistence"""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# ------------------------------------------------------------------------------------------------ #
def wireup() -> None:
    """Wires the container, injecting dependencies as specified"""
    container = AppStoreContainer()
    container.init_resources()
    container.wire(
        modules=[
            __name__,
            "aimobile.scraper.appstore.container",
            "aimobile.scraper.appstore.repo.datacentre",
            "aimobile.scraper.appstore.service.review",
            "aimobile.scraper.appstore.service.appdata",
            "aimobile.scraper.appstore.service.rating",
        ]
    )


# ------------------------------------------------------------------------------------------------ #
def main() -> None:
    make_directories()
    wireup()


# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    main()
