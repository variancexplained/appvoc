/*
 * Filename: /home/john/projects/aimobile/aimobile/scraper/appstore/database/review.sql
 * Path: /home/john/projects/aimobile/notes
 * Created Date: Tuesday, April 11th 2023, 12:25:10 am
 * Author: John James
 *
 * Copyright (c) 2023 John James
 */


CREATE DATABASE aimobile;

USE aimobile;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `review`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `review` (
    `id` INTEGER NOT NULL,
    `app_id` INTEGER NOT NULL,
    `category_id` INTEGER NOT NULL,
    `category` VARCHAR(32) NOT NULL,
    `author` VARCHAR(128) NOT NULL,
    `rating` FLOAT NOT NULL,
    `title` VARCHAR(128) NOT NULL,
    `content` MEDIUMTEXT NOT NULL,
    `vote_sum` BIGINT NOT NULL,
    `vote_count` BIGINT NOT NULL,
    `date` DATETIME NOT NULL,
    `source` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`)
);
