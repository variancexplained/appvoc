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
# Modified   : Wednesday August 9th 2023 02:25:06 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from appstore.data.acquisition.base import Director
from appstore.data.acquisition.base import Job
from appstore.data.acquisition.rating.job import RatingJobRun
from appstore.data.storage.uow import UoW


# ------------------------------------------------------------------------------------------------ #
class RatingDirector(Director):
    """Iterator serving jobs to the controller."""

    def __init__(self, uow: UoW) -> None:
        super().__init__(uow=uow)

    def add_jobrun(self, jobrun: RatingJobRun) -> None:
        """Adds a job run to the repository.

        Args:
            jobrun (RatingJobRun): Job run object
        """
        self._uow.rating_jobrun_repo.add(jobrun=jobrun)
        self._uow.save()

    def update_jobrun(self, jobrun: RatingJobRun) -> None:
        """Updates the jobrun repository

        Args:
            jobrun (RatingJobRun): Job run object
        """
        self._uow.rating_jobrun_repo.update(jobrun=jobrun)
        self._uow.save()

    def update_job(self, job: Job) -> None:
        """Updates a job in the repository.

        Args:
            job (Job): Job object
        """
        self._uow.job_repo.update(job=job)
        self._uow.save()

    def next(self) -> RatingJobRun:
        """Sets the next job and returns an instance of this iterator"""

        job = self._uow.job_repo.next(controller="RatingController")
        if job is not None:
            return RatingJobRun.from_job(job=job)
        else:
            return None
