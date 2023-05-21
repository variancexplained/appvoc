#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/dataset/appdata.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 21st 2023 03:53:33 am                                                    #
# Modified   : Sunday May 21st 2023 04:15:31 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #

from dependency_injector.wiring import Provide, inject

from aimobile.data.repo.base import Repo
from aimobile.data.dataset.base import Dataset
from aimobile.container import AIMobileContainer


# ------------------------------------------------------------------------------------------------ #
class AppDataDataset(Dataset):
    """An in-memory dataset containing app data

    Args:
        repo (Repo): The dataset repository
    """

    @inject
    def __init__(self, repo: Repo = Provide[AIMobileContainer.data.appdata_repo]) -> None:
        super().__init__(repo=repo)

    @property
    def summary(self) -> None:
        """Summarizes the data"""

        summary = self._df["category"].value_counts().reset_index()
        summary.columns = ["category", "Examples"]
        df2 = self._df.groupby(by="category")["id"].nunique().to_frame()
        df3 = self._df.groupby(by="category")["rating"].mean().to_frame()
        df4 = self._df.groupby(by="category")["ratings"].sum().to_frame()

        summary = summary.join(df2, on="category")
        summary = summary.join(df3, on="category")
        summary = summary.join(df4, on="category")
        summary.columns = ["Category", "Examples", "Apps", "Average Rating", "Rating Count"]
        return summary
