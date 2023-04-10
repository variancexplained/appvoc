#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 01:06:35 am                                                  #
# Modified   : Monday April 10th 2023 01:34:29 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from aimobile.scraper.appstore.container import AppStoreContainer


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
            "aimobile.scraper.appstore.internet.request",
            "aimobile.scraper.appstore.service.appdata",
        ]
    )


# ------------------------------------------------------------------------------------------------ #
def main() -> None:
    wireup()


# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    main()
