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
# Modified   : Wednesday August 2nd 2023 05:17:17 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from appstore.data.acquisition.base import Director
from appstore.data.acquisition.review.job import ReviewJobRun
from appstore.data.storage.job import ReviewJobRunRepo, JobRepo


# ------------------------------------------------------------------------------------------------ #
class ReviewDirector(Director):
    """Iterator serving jobs to the controller."""

    def __init__(self, jobrun_repo: ReviewJobRunRepo, job_repo: JobRepo) -> None:
        super().__init__(jobrun_repo=jobrun_repo, job_repo=job_repo)

    def __iter__(self) -> ReviewDirector:
        """Initializes the job iterator"""
        return self

    def __next__(self) -> ReviewDirector:
        """Sets the next job and returns an instance of this iterator"""
        jobrun = self._jobrun_repo.next()
        if jobrun is not None:
            return ReviewJobRun.from_jobrun(jobrun=jobrun)
        else:
            job = self._job_repo.next(controller="ReviewController")
            if job is not None:
                return ReviewJobRun.from_job(job=job)
            else:
                raise StopIteration
