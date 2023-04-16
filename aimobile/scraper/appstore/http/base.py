#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/http/base.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:22:06 am                                                 #
# Modified   : Sunday April 16th 2023 04:40:07 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from aimobile.scraper.base import RequestIterator, Handler  # noqa: F401
from enum import Enum


# ------------------------------------------------------------------------------------------------ #
class SessionResponse(Enum):
    SUCCESS = 0
    RETRY = 1
    GRACEFUL_EXIT = 2
    IGNITE_HAIR = 3


# ------------------------------------------------------------------------------------------------ #
class HTTPVars:
    TIMEOUT = 30
    TOTAL_RETRIES = 5
    SESSIONS = 3
    MAX_PAGES = 99999
    LIMIT = 200
    EPOCH = 40246871
    DELAY_MIN = 1
    DELAY_MAX = 8
    BACKOFF_FACTOR = 2
    STATUS_FORCELIST = [104, 429, 500, 502, 503, 504]
    METHOD_WHITELIST = ["HEAD", "GET" "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    RAISE_ON_REDIRECT = False
    RAISE_ON_STATUS = False
    ALLOWED_ANOMALIES = 5
    DONE = 222
    NO_CONTENT = 204


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
STOREFRONTS = [
    {"country": "us", "headers": {"X-Apple-Store-Front": "143441-1,29"}},
    {"country": "au", "headers": {"X-Apple-Store-Front": "143460,29"}},
    {"country": "ca", "headers": {"X-Apple-Store-Front": "143455-6,29"}},
    {"country": "gb", "headers": {"X-Apple-Store-Front": "143444,29"}},
]
# ------------------------------------------------------------------------------------------------ #
# Servers provided courtesy of https://github.com/clarketm/proxy-list
SERVERS = [
    "rotating-residential.geonode.com:9000",
    "rotating-residential.geonode.com:9001",
    "rotating-residential.geonode.com:9002",
    "rotating-residential.geonode.com:9003",
    "rotating-residential.geonode.com:9004",
    "rotating-residential.geonode.com:9005",
    "rotating-residential.geonode.com:9006",
    "rotating-residential.geonode.com:9007",
    "rotating-residential.geonode.com:9008",
    "rotating-residential.geonode.com:9009",
    "rotating-residential.geonode.com:9010",
]
