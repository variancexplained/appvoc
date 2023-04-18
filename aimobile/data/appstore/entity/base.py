#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/entity/base.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 09:57:42 am                                                 #
# Modified   : Saturday April 15th 2023 11:05:39 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module containing Appstore categories and groupings."""


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


class AppStoreCategories:
    """
    App Store category IDs

    Borrowed from https://github.com/facundoolano/app-store-scraper. These are
    the app's categories.
    """

    BOOKS = 6018
    BUSINESS = 6000
    CATALOGS = 6022
    EDUCATION = 6017
    ENTERTAINMENT = 6016
    FINANCE = 6015
    FOOD_AND_DRINK = 6023
    GAMES = 6014
    GAMES_ACTION = 7001
    GAMES_ADVENTURE = 7002
    GAMES_ARCADE = 7003
    GAMES_BOARD = 7004
    GAMES_CARD = 7005
    GAMES_CASINO = 7006
    GAMES_DICE = 7007
    GAMES_EDUCATIONAL = 7008
    GAMES_FAMILY = 7009
    GAMES_MUSIC = 7011
    GAMES_PUZZLE = 7012
    GAMES_RACING = 7013
    GAMES_ROLE_PLAYING = 7014
    GAMES_SIMULATION = 7015
    GAMES_SPORTS = 7016
    GAMES_STRATEGY = 7017
    GAMES_TRIVIA = 7018
    GAMES_WORD = 7019
    HEALTH_AND_FITNESS = 6013
    LIFESTYLE = 6012
    MAGAZINES_AND_NEWSPAPERS = 6021
    MAGAZINES_ARTS = 13007
    MAGAZINES_AUTOMOTIVE = 13006
    MAGAZINES_WEDDINGS = 13008
    MAGAZINES_BUSINESS = 13009
    MAGAZINES_CHILDREN = 13010
    MAGAZINES_COMPUTER = 13011
    MAGAZINES_FOOD = 13012
    MAGAZINES_CRAFTS = 13013
    MAGAZINES_ELECTRONICS = 13014
    MAGAZINES_ENTERTAINMENT = 13015
    MAGAZINES_FASHION = 13002
    MAGAZINES_HEALTH = 13017
    MAGAZINES_HISTORY = 13018
    MAGAZINES_HOME = 13003
    MAGAZINES_LITERARY = 13019
    MAGAZINES_MEN = 13020
    MAGAZINES_MOVIES_AND_MUSIC = 13021
    MAGAZINES_POLITICS = 13001
    MAGAZINES_OUTDOORS = 13004
    MAGAZINES_FAMILY = 13023
    MAGAZINES_PETS = 13024
    MAGAZINES_PROFESSIONAL = 13025
    MAGAZINES_REGIONAL = 13026
    MAGAZINES_SCIENCE = 13027
    MAGAZINES_SPORTS = 13005
    MAGAZINES_TEENS = 13028
    MAGAZINES_TRAVEL = 13029
    MAGAZINES_WOMEN = 13030
    MEDICAL = 6020
    MUSIC = 6011
    NAVIGATION = 6010
    NEWS = 6009
    PHOTO_AND_VIDEO = 6008
    PRODUCTIVITY = 6007
    REFERENCE = 6006
    SHOPPING = 6024
    SOCIAL_NETWORKING = 6005
    SPORTS = 6004
    TRAVEL = 6003
    UTILITIES = 6002
    WEATHER = 6001


class AppStoreCategoryIds:
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
