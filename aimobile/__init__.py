#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/__init__.py                                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:28:06 pm                                                  #
# Modified   : Wednesday May 17th 2023 05:18:33 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass


@dataclass
class Palette:
    name: str = "Blues_r"
    color: str = "#69d"
    reverse: bool = True
    as_cmap: bool = True


# ------------------------------------------------------------------------------------------------ #
class Visual:
    style = "whitegrid"
    palette = Palette
    figsize = (12, 3)
