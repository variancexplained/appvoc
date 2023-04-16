#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/database/mongo.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 06:46:30 pm                                                  #
# Modified   : Monday April 10th 2023 09:36:46 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""MongoDB Module"""
import os
from dotenv import load_dotenv
import logging
from typing import Union

from pymongo import MongoClient
import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class MongoDB:
    """Mongo Database"""

    def __init__(self, name: str) -> None:
        self._name = name
        load_dotenv()
        self._connection_string = os.getenv("MONGO")
        self._connection = None
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def connect(self) -> None:
        self._connection = MongoClient(self._connection_string)
        self._database = self._connection[self._name]
        return self._database

    def close(self) -> None:
        self._connection.close()

    def get_create_collection(self, name) -> MongoClient.collection:
        return self._database[name]

    def insert(self, data: pd.DataFrame, collection: MongoClient.collection) -> None:
        data = data.reset_index()
        data_dict = data.to_dict()
        collection.insert_many(data_dict)

    def list(self, collection: MongoClient.collection) -> list[MongoClient.document]:
        return collection.list_collection_names()

    def query(
        self, key: str, value: Union[int, str], collection: MongoClient.collection
    ) -> MongoClient.document:
        query = {key: value}
        return collection.find(query)
