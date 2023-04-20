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
# Modified   : Tuesday April 18th 2023 01:53:24 pm                                                 #
# Modifier : John James (john.james.ai.studio@gmail.com)                                           #
# ------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                               #
# Copyright: (c) 2022 Bryant St. Labs                                                              #
# ================================================================================================ #
echo $'\nRestart MySQL...'
sudo /etc/init.d/mysql restart

echo $'\nSetup User...'
sudo mysql -u root -p --database mysql < /home/john/projects/aimobile/scripts/database/setup/user.sql


echo $'\nBuilding Databases...'
sudo mysql -u root -p --database mysql < /home/john/projects/aimobile/scripts/database/setup/build.sql

echo $'\nStopping MySQL...'
sudo /etc/init.d/mysql stop
