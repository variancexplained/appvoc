/*
 * Filename: /home/john/projects/aimobile/scripts/database/setup/build_googleplay.sql
 * Path: /home/john/projects/aimobile/notes
 * Created Date: Tuesday, April 11th 2023, 12:25:10 am
 * Author: John James
 *
 * Copyright (c) 2023 John James
 */

CREATE DATABASE IF NOT EXISTS googleplay_prod;
CREATE DATABASE IF NOT EXISTS googleplay_dev;
CREATE DATABASE IF NOT EXISTS googleplay_test;

/*Build review tables with long text */
USE googleplay_prod;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `review`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `review` (
    `id` VARCHAR(256) NOT NULL,
    `app_id` VARCHAR(256) NOT NULL,
    `author` VARCHAR(128) NOT NULL,
    `score` FLOAT NOT NULL,
    `content` LONGTEXT NOT NULL,
    `thumbs_up` INTEGER NOT NULL,
    `date` DATETIME NOT NULL,
    `source` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`)
);

USE googleplay_dev;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `review`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `review` (
    `id` VARCHAR(256) NOT NULL,
    `app_id` VARCHAR(256) NOT NULL,
    `author` VARCHAR(128) NOT NULL,
    `score` FLOAT NOT NULL,
    `content` LONGTEXT NOT NULL,
    `thumbs_up` INTEGER NOT NULL,
    `date` DATETIME NOT NULL,
    `source` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`)
);

USE googleplay_test;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `review`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `review` (
    `id` VARCHAR(256) NOT NULL,
    `app_id` VARCHAR(256) NOT NULL,
    `author` VARCHAR(128) NOT NULL,
    `score` FLOAT NOT NULL,
    `content` LONGTEXT NOT NULL,
    `thumbs_up` INTEGER NOT NULL,
    `date` DATETIME NOT NULL,
    `source` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`)
);

