#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/conftest.py                                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:01:48 pm                                                  #
# Modified   : Tuesday April 18th 2023 01:19:45 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pytest

from aimobile.framework.io.local import IOService
from aimobile.framework.container import FrameworkContainer


# ================================================================================================ #
#                                FRAMEWORK TEST FIXTURES                                           #
# ================================================================================================ #

DATAFRAME_FILEPATH = "tests/data/test.csv"


# ------------------------------------------------------------------------------------------------ #
#                                 DATABASE FIXTURES                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="session", autouse=True)
def dataframe():
    df = IOService.read(DATAFRAME_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="session", autouse=True)
def framework():
    container = FrameworkContainer()
    container.init_resources()
    return container
