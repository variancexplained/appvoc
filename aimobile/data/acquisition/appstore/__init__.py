#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/service/appstore/__init__.py                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:37:58 pm                                                  #
# Modified   : Thursday April 27th 2023 03:08:49 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                        BROWSER HEADERS                                           #
# ------------------------------------------------------------------------------------------------ #
HEADERS = [
    {
        "authority": "www.apple.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": "geo=US; s_fid=06052E4035BD477E-287EA4F0D67179DA; s_cc=true; mk_epub=%7B%22btuid%22%3A%221p309rf%22%2C%22prop57%22%3A%22www.us.itunes%22%7D; s_vi=[CS]v1|32164EB46DD3A424-60001FE203923437[CE]; pt-dm=v1~x~90ni8h34~m~1~n~itunes%20-%20index%20(us)",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    },
    {
        "authority": "www.apple.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": "geo=US; s_fid=06052E4035BD477E-287EA4F0D67179DA; s_cc=true; mk_epub=%7B%22btuid%22%3A%221p309rf%22%2C%22prop57%22%3A%22www.us.itunes%22%7D; s_vi=[CS]v1|32164EB46DD3A424-60001FE203923437[CE]; pt-dm=v1~x~90ni8h34~m~1~n~itunes%20-%20index%20(us)",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="110", "Not(A:Brand";v="8", "Chromium";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:111.0) Gecko/20100101 Firefox/111.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    },
    {
        "authority": "www.apple.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "geo=US; s_fid=30A04E3CF3D9F051-1CE913ACD3B58514; s_cc=true; mk_epub=%7B%22btuid%22%3A%2262q2jj%22%2C%22prop57%22%3A%22www.us.itunes%22%7D; s_vi=[CS]v1|321651851683436F-40001437604D6F47[CE]; pt-dm=v1~x~za8r1msw~m~1~n~itunes%20-%20index%20(us)",
        "sec-ch-ua": '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    },
    {
        "authority": "www.apple.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "geo=US; s_fid=30A04E3CF3D9F051-1CE913ACD3B58514; s_cc=true; mk_epub=%7B%22btuid%22%3A%2262q2jj%22%2C%22prop57%22%3A%22www.us.itunes%22%7D; s_vi=[CS]v1|321651851683436F-40001437604D6F47[CE]; pt-dm=v1~x~za8r1msw~m~1~n~itunes%20-%20index%20(us)",
        "sec-ch-ua": '"Microsoft Edge";v="110", "Not(A:Brand";v="8", "Chromium";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    },
    {
        "authority": "www.apple.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "geo=US; s_fid=037BA24B83F1E75D-00847AB1DC3C8B16; s_cc=true; mk_epub=%7B%22btuid%22%3A%22v2gsww%22%2C%22prop57%22%3A%22www.us.itunes%22%7D; pt-dm=v1~x~es8yixh8~m~1~n~itunes%20-%20index%20(us)",
        "sec-ch-ua": '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0",
    },
]
# ------------------------------------------------------------------------------------------------ #
#                               APPSTORE STOREFRONT HEADERS                                        #
# ------------------------------------------------------------------------------------------------ #
STOREFRONTS = [
    {"country": "us", "headers": {"X-Apple-Store-Front": "143441-1,29"}},
    {"country": "au", "headers": {"X-Apple-Store-Front": "143460,29"}},
    {"country": "ca", "headers": {"X-Apple-Store-Front": "143455-6,29"}},
    {"country": "gb", "headers": {"X-Apple-Store-Front": "143444,29"}},
]

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
