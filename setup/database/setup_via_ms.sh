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
# Modified   : Thursday April 13th 2023 05:51:21 pm                                                #
# Modifier : John James (john.james.ai.studio@gmail.com)                                           #
# ------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                               #
# Copyright: (c) 2022 Bryant St. Labs                                                              #
# ================================================================================================ #
echo $'\nStop MySQL processes..'
sudo /etc/init.d/mysql stop

echo $'\nRemoving existing installation..'
sudo apt purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-* -y
sudo apt-get remove mysql-* -y
sudo apt-get purge mysql-* -y
sudo apt remove dbconfig-mysql -y

echo $'\nDelete all MySQL files...'
sudo rm -rf /etc/mysql /var/lib/mysql /var/log/mysql

echo $'\nCleaning packages not needed...'
sudo apt-get autoclean -y
sudo apt autoremove -y
sudo apt autoclean -y
# Follow instructions at https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-database
# use wsl terminal

echo $'\nUpdating ubuntu packages...'
sudo apt update -y

echo $'\nInstall MySQL'
sudo apt install mysql-server

echo $'\nStart the server'
sudo /etc/init.d/mysql start

echo $'\nSetup User...'
sudo mysql -u root -p --database mysql < /home/john/projects/aimobile/setup/database/user.sql

echo $'\nSetup Database'
sudo mysql -u root -p --database mysql < /home/john/projects/aimobile/aimobile/scraper/appstore/database/review.sql

echo $'\nLaunch MySQL'
sudo mysql -u root -p