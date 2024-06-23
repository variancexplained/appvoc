#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/dataset/review.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 21st 2023 03:53:33 am                                                    #
# Modified   : Monday August 28th 2023 05:31:38 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd
from studioai.data.dataset import Dataset

from appvoc.data.entity.review import Review


# ------------------------------------------------------------------------------------------------ #
class ReviewDataset(Dataset):
    """An in-memory dataset containing app data

    Args:
        repo (Repo): The dataset repository
    """

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df=df)

    def __getitem__(self, idx: int) -> Review:
        df = self._df.iloc[[idx]]
        return Review.from_df(df=df)

    def summary(self) -> pd.DataFrame:
        """Summarizes the app data by category"""
        df2 = self._df.groupby(["category"])["id"].nunique().to_frame()
        df3 = self._df.groupby(["category"])["app_id"].nunique().to_frame()
        summary = df2.join(df3, on="category").reset_index()
        summary.columns = ["Category", "Reviews", "Apps"]
        return summary
