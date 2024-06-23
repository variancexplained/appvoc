#!/usr/bin/bash
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project  : DeepCTR: Deep Learning and Neural Architecture Selection for CTR Prediction           #
# Version  : 0.1.0                                                                                 #
# File     : /setup.sh                                                                             #
# Language : Python 3.7.12                                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                            #
# Email    : john@variancexplained.com                                                        #
# URL      : https://github.com/variancexplained/DeepCTR                                              #
# ------------------------------------------------------------------------------------------------ #
# Created  : Thursday, April 21st 2022, 9:02:53 am                                                 #
# Modified   : Friday August 25th 2023 10:27:43 am                                                 #
# Modifier : John James (john@variancexplained.com)                                           #
# ------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                               #
# Copyright: (c) 2022 Bryant St. Labs                                                              #
# ================================================================================================ #
# echo $'\nRestart MySQL...'
# sudo /etc/init.d/mysql restart

# echo $'\nSetup User...'
# sudo mysql -u root -p --database mysql < /home/john/projects/appvoc/scripts/database/setup/user.sql


echo $'\nBuilding Databases...'
sudo mysql -u root -p --database mysql < /home/john/projects/appvoc/scripts/database/setup/build.sql

# echo $'\nStopping MySQL...'
# sudo /etc/init.d/mysql stop
