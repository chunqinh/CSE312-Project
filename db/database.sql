CREATE DATABASE IF NOT EXISTS 312project_db;
use 312project_db;


CREATE TABLE IF NOT EXISTS `user` (
    `username` VARCHAR(99) NOT NULL,
    `password` VARCHAR(99) NOT NULL,
    `is_online` BOOLEAN DEFAULT FALSE,
    `username_color` VARCHAR(99) DEFAULT '#000000',
    `bio` VARCHAR(99) DEFAULT 'No Bio',
    PRIMARY KEY (`username`)
);


CREATE TABLE IF NOT EXISTS `voting` (
    `vote_ID` INT NOT NULL AUTO_INCREMENT,
    `creator_username` VARCHAR(99) NOT NULL,
    `vote_name` VARCHAR(99) NOT NULL,
    `vote_description` VARCHAR(99) NOT NULL,
    `photo` VARCHAR(99),
    `option_one_name` VARCHAR(99) NOT NULL,
    `option_one_votes` INT DEFAULT 0,
    `option_two_name` VARCHAR(99) NOT NULL,
    `option_two_votes` INT DEFAULT 0,
    `option_three_name` VARCHAR(99) DEFAULT NULL,
    `option_three_votes` INT DEFAULT 0,
    `option_four_name` VARCHAR(99) DEFAULT NULL,
    ` option_four_votes` INT DEFAULT 0,
    `option_five_name` VARCHAR(99) DEFAULT NULL,
    `option_five_votes` INT DEFAULT 0,
    PRIMARY KEY (`vote_ID`),
    FOREIGN KEY (`creator_username`) REFERENCES `user`(`username`)
);


CREATE TABLE IF NOT EXISTS `message` (
    `message_ID` INT NOT NULL AUTO_INCREMENT,
    `sender_username` VARCHAR(99) NOT NULL,
    `receiver_username` VARCHAR(99) NOT NULL,
    `content` VARCHAR(999) NOT NULL,
    `message_time` DATETIME NOT NULL,
    PRIMARY KEY (`message_ID`),
    FOREIGN KEY (`sender_username`) REFERENCES `user`(`username`),
    FOREIGN KEY (`receiver_username`) REFERENCES `user`(`username`)
);