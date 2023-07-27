#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.8                                                                              #
# Filename   : /appstore/data/repo/__init__.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:37:58 pm                                                  #
# Modified   : Tuesday July 25th 2023 03:50:18 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Contains Package Constants """
from sqlalchemy.dialects.mysql import (
    MEDIUMTEXT,
    LONGTEXT,
    BIGINT,
    VARCHAR,
    INTEGER,
    FLOAT,
)

# ================================================================================================ #
#                                          APPSTORE                                                #
# ================================================================================================ #
#                                           APPDATA                                                #
# ------------------------------------------------------------------------------------------------ #
APPSTORE_APPDATA_DTYPES = {
    "id": BIGINT,
    "name": VARCHAR(256),
    "description": LONGTEXT,
    "category_id": INTEGER,
    "category": VARCHAR(128),
    "price": FLOAT,
    "developer_id": BIGINT,
    "developer": VARCHAR(256),
    "rating": FLOAT,
    "ratings": BIGINT,
    "released": VARCHAR(32),
}

APPSTORE_APPDATA_VTYPES = {
    "id": "discrete",
    "name": "nominal",
    "description": "nominal",
    "category_id": "discrete",
    "category": "nominal",
    "price": "continuous",
    "developer_id": "discrete",
    "developer": "nominal",
    "rating": "continuous",
    "ratings": "discrete",
    "released": "discrete",
}
# ------------------------------------------------------------------------------------------------ #
#                                            REVIEW                                                #
# ------------------------------------------------------------------------------------------------ #
APPSTORE_REVIEW_DTYPES = {
    "id": BIGINT,
    "app_id": BIGINT,
    "app_name": VARCHAR(128),
    "category_id": INTEGER,
    "category": VARCHAR(128),
    "author": VARCHAR(128),
    "rating": FLOAT,
    "title": VARCHAR(256),
    "content": LONGTEXT,
    "vote_sum": BIGINT,
    "vote_count": BIGINT,
    "date": VARCHAR(32),
}

APPSTORE_REVIEW_VTYPES = {
    "id": "discrete",
    "app_id": "discrete",
    "app_name": "nominal",
    "category_id": "discrete",
    "category": "nominal",
    "author": "nominal",
    "rating": "continuous",
    "title": "nominal",
    "content": "nominal",
    "vote_sum": "discrete",
    "vote_count": "discrete",
    "date": "discrete",
}

# ------------------------------------------------------------------------------------------------ #
#                                            RATING                                                #
# ------------------------------------------------------------------------------------------------ #
APPSTORE_RATING_DTYPES = {
    "id": BIGINT,
    "name": VARCHAR(128),
    "category_id": INTEGER,
    "category": VARCHAR(64),
    "rating": FLOAT,
    "reviews": BIGINT,
    "ratings": BIGINT,
    "onestar": BIGINT,
    "twostar": BIGINT,
    "threestar": BIGINT,
    "fourstar": BIGINT,
    "fivestar": BIGINT,
}

APPSTORE_RATING_VTYPES = {
    "id": "discrete",
    "name": "nominal",
    "category_id": "discrete",
    "category": "nominal",
    "rating": "continous",
    "reviews": "discrete",
    "ratings": "discrete",
    "onestar": "discrete",
    "twostar": "discrete",
    "threestar": "discrete",
    "fourstar": "discrete",
    "fivestar": "discrete",
}

# ------------------------------------------------------------------------------------------------ #
#                                           APPSTORE                                               #
# ------------------------------------------------------------------------------------------------ #
APPSTORE_DTYPES = {
    "id": BIGINT,
    "name": VARCHAR(128),
    "category_id": INTEGER,
    "category": VARCHAR(64),
    "price": FLOAT,
    "rating": FLOAT,
    "reviews": BIGINT,
    "ratings": BIGINT,
    "onestar": BIGINT,
    "twostar": BIGINT,
    "threestar": BIGINT,
    "fourstar": BIGINT,
    "fivestar": BIGINT,
}

APPSTORE_VTYPES = {
    "id": "discrete",
    "name": "nominal",
    "category_id": "discrete",
    "category": "nominal",
    "price": "continuous",
    "rating": "continous",
    "reviews": "discrete",
    "ratings": "discrete",
    "onestar": "discrete",
    "twostar": "discrete",
    "threestar": "discrete",
    "fourstar": "discrete",
    "fivestar": "discrete",
}
