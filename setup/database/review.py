#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /setup/database/review.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 11th 2023 12:32:35 am                                                 #
# Modified   : Thursday April 13th 2023 07:53:48 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Review DDL Module"""
# %%
from aimobile.scraper.appstore.database.mysql import MySQLDatabase
import logging

FILEPATH = "/home/john/projects/aimobile/setup/database/review.sql"
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #


def build_reviews(filepath: str):
    database = MySQLDatabase(name="aimobile")

    with open(filepath, "r") as sqlfile:
        with database as db:
            results = db.executemulti(sqlfile.read())
            for result in results:
                logger.info(f"Running query: {result}")
                logger.info(f"Rows affected: {result.rowcount}")


# ------------------------------------------------------------------------------------------------ #
def main(filepath: str) -> None:
    build_reviews(filepath)


# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    main(FILEPATH)
