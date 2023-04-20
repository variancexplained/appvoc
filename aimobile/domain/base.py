#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/domain/base.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 09:57:42 am                                                 #
# Modified   : Thursday April 20th 2023 12:41:05 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module containing Appstore categories and groupings."""
from dataclasses import dataclass
from abc import ABC, abstractclassmethod
from datetime import datetime

import pandas as pd

# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)


# ------------------------------------------------------------------------------------------------ #
#                                        ENTITY                                                    #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Entity(ABC):
    """Abstract base class which defines the interface for entity classes."""

    @abstractclassmethod
    def from_dict(cls) -> pd.DataFrame:
        """Creates an entity from a dictionary of attributes."""

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the parameter object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v.strftime("%m/%d/%Y, %H:%M:%S")
        elif isinstance(v, dict):
            return {kk: cls._export_config(vv) for kk, vv in v}
        else:
            try:
                return v.__class__.__name__
            except:  # noqa 722
                return "Mutable Object"


# ------------------------------------------------------------------------------------------------ #
#                                       COLLECTIONS                                                #
# ------------------------------------------------------------------------------------------------ #


class AppStoreCollections:
    """
    App store collection IDs

    Borrowed from https://github.com/facundoolano/app-store-scraper. These are
    the various collections displayed in the app store, usually on the front
    page.
    """

    TOP_MAC = "topmacapps"
    TOP_FREE_MAC = "topfreemacapps"
    TOP_GROSSING_MAC = "topgrossingmacapps"
    TOP_PAID_MAC = "toppaidmacapps"
    NEW_IOS = "newapplications"
    NEW_FREE_IOS = "newfreeapplications"
    NEW_PAID_IOS = "newpaidapplications"
    TOP_FREE_IOS = "topfreeapplications"
    TOP_FREE_IPAD = "topfreeipadapplications"
    TOP_GROSSING_IOS = "topgrossingapplications"
    TOP_GROSSING_IPAD = "topgrossingipadapplications"
    TOP_PAID_IOS = "toppaidapplications"
    TOP_PAID_IPAD = "toppaidipadapplications"


# ------------------------------------------------------------------------------------------------ #
#                                       CATEGORIES                                                 #
# ------------------------------------------------------------------------------------------------ #
class AppStoreCategories:
    NAMES = {
        6018: "BOOKS",
        6000: "BUSINESS",
        6022: "CATALOGS",
        6017: "EDUCATION",
        6016: "ENTERTAINMENT",
        6015: "FINANCE",
        6023: "FOOD_AND_DRINK",
        6014: "GAMES",
        7001: "GAMES_ACTION",
        7002: "GAMES_ADVENTURE",
        7003: "GAMES_ARCADE",
        7004: "GAMES_BOARD",
        7005: "GAMES_CARD",
        7006: "GAMES_CASINO",
        7007: "GAMES_DICE",
        7008: "GAMES_EDUCATIONAL",
        7009: "GAMES_FAMILY",
        7011: "GAMES_MUSIC",
        7012: "GAMES_PUZZLE",
        7013: "GAMES_RACING",
        7014: "GAMES_ROLE_PLAYING",
        7015: "GAMES_SIMULATION",
        7016: "GAMES_SPORTS",
        7017: "GAMES_STRATEGY",
        7018: "GAMES_TRIVIA",
        7019: "GAMES_WORD",
        6013: "HEALTH_AND_FITNESS",
        6012: "LIFESTYLE",
        6021: "MAGAZINES_AND_NEWSPAPERS",
        13007: "MAGAZINES_ARTS",
        13006: "MAGAZINES_AUTOMOTIVE",
        13008: "MAGAZINES_WEDDINGS",
        13009: "MAGAZINES_BUSINESS",
        13010: "MAGAZINES_CHILDREN",
        13011: "MAGAZINES_COMPUTER",
        13012: "MAGAZINES_FOOD",
        13013: "MAGAZINES_CRAFTS",
        13014: "MAGAZINES_ELECTRONICS",
        13015: "MAGAZINES_ENTERTAINMENT",
        13002: "MAGAZINES_FASHION",
        13017: "MAGAZINES_HEALTH",
        13018: "MAGAZINES_HISTORY",
        13003: "MAGAZINES_HOME",
        13019: "MAGAZINES_LITERARY",
        13020: "MAGAZINES_MEN",
        13021: "MAGAZINES_MOVIES_AND_MUSIC",
        13001: "MAGAZINES_POLITICS",
        13004: "MAGAZINES_OUTDOORS",
        13023: "MAGAZINES_FAMILY",
        13024: "MAGAZINES_PETS",
        13025: "MAGAZINES_PROFESSIONAL",
        13026: "MAGAZINES_REGIONAL",
        13027: "MAGAZINES_SCIENCE",
        13005: "MAGAZINES_SPORTS",
        13028: "MAGAZINES_TEENS",
        13029: "MAGAZINES_TRAVEL",
        13030: "MAGAZINES_WOMEN",
        6020: "MEDICAL",
        6011: "MUSIC",
        6010: "NAVIGATION",
        6009: "NEWS",
        6008: "PHOTO_AND_VIDEO",
        6007: "PRODUCTIVITY",
        6006: "REFERENCE",
        6024: "SHOPPING",
        6005: "SOCIAL_NETWORKING",
        6004: "SPORTS",
        6003: "TRAVEL",
        6002: "UTILITIES",
        6001: "WEATHER",
    }
