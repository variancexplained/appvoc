#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/review/director.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 30th 2023 05:32:24 pm                                                   #
# Modified   : Thursday August 10th 2023 11:33:05 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from appstore.data.acquisition.base import Director
from appstore.data.acquisition.base import Job
from appstore.data.acquisition.review.job import ReviewJobRun
from appstore.data.repo.uow import UoW


# ------------------------------------------------------------------------------------------------ #
class ReviewDirector(Director):
    """Iterator serving jobs to the controller."""

    def __init__(self, uow: UoW) -> None:
        super().__init__(uow=uow)

    def add_jobrun(self, jobrun: ReviewJobRun) -> None:
        """Adds a job run to the repository.

        Args:
            jobrun (ReviewJobRun): Job run object
        """
        self._uow.review_jobrun_repo.add(jobrun=jobrun)
        self._uow.save()

    def update_jobrun(self, jobrun: ReviewJobRun) -> None:
        """Updates the jobrun repository

        Args:
            jobrun (ReviewJobRun): Job run object
        """
        self._uow.review_jobrun_repo.update(jobrun=jobrun)
        self._uow.save()

    def update_job(self, job: Job) -> None:
        """Updates a job in the repository.

        Args:
            job (Job): Job object
        """
        self._uow.job_repo.update(job=job)
        self._uow.save()

    def next(self) -> ReviewJobRun:
        """Sets the next job and returns an instance of this iterator"""

        job = self._uow.job_repo.next(controller="ReviewController")
        if job is not None:
            return ReviewJobRun.from_job(job=job)
        else:
            return None
