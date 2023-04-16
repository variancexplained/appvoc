#!/usr/bin/bash
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project  : DeepCTR: Deep Learning and Neural Architecture Selection for CTR Prediction           #
# Version  : 0.1.0                                                                                 #
# File     : /setup.sh                                                                             #
# Language : Python 3.7.12                                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                            #
# Email    : john.james.ai.studio@gmail.com                                                        #
# URL      : https://github.com/john-james-ai/DeepCTR                                              #
# ------------------------------------------------------------------------------------------------ #
# Created  : Thursday, April 21st 2022, 9:02:53 am                                                 #
# Modified   : Thursday April 13th 2023 05:58:31 pm                                                #
# Modifier : John James (john.james.ai.studio@gmail.com)                                           #
# ------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                               #
# Copyright: (c) 2022 Bryant St. Labs                                                              #
# ================================================================================================ #
echo $'\nSetup User and Databases...'
sudo mysql -u root -p --database mysql < /home/john/projects/aimobile/aimobile/scraper/appstore/database/review.sql

