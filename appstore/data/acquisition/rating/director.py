#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/rating/director.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 30th 2023 05:32:24 pm                                                   #
# Modified   : Sunday July 30th 2023 08:35:32 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from appstore.data.acquisition.base import Director
from appstore.data.storage.job import RatingJobRepo


# ------------------------------------------------------------------------------------------------ #
class RatingDirector(Director):
    """Iterator serving jobs to the controller."""

    def __init__(self, repo: RatingJobRepo) -> None:
        super().__init__(repo=repo)

    def __iter__(self) -> RatingDirector:
        """Initializes the job iterator"""
        return self

    def __next__(self) -> RatingDirector:
        """Sets the next job and returns an instance of this iterator"""
        job = self._repo.next()
        if job:
            return self
        else:
            raise StopIteration
