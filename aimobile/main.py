#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/main.py                                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:25:30 am                                                #
# Modified   : Wednesday April 5th 2023 04:32:52 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from aimobile.container import AIMobile


# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    container = AIMobile()
    container.init_resources()
    container.wire(modules=[__name__, "aimobile.data.scraper.appstore.dal.datacentre"])
