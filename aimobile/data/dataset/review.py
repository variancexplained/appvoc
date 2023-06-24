#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /aimobile/data/dataset/review.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 21st 2023 03:53:33 am                                                    #
# Modified   : Saturday June 24th 2023 01:48:03 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd
from dependency_injector.wiring import Provide, inject

from aimobile.data.repo.base import Repo
from aimobile.data.dataset.base import Dataset
from aimobile.container import AIMobileContainer


# ------------------------------------------------------------------------------------------------ #
class ReviewDataset(Dataset):
    """An in-memory dataset containing app data

    Args:
        repo (Repo): The dataset repository
    """

    @inject
    def __init__(self, repo: Repo = Provide[AIMobileContainer.data.review_repo]) -> None:
        super().__init__(repo=repo)

    @property
    def summary(self) -> pd.DataFrame:
        """Summarizes the number of reviews."""
        return self._repo.summary()
