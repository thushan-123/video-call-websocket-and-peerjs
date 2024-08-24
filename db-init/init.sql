CREATE DATABASE IF NOT EXISTS edexme_db;
USE edexme_db;

-- Create the 'user' table
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `trainer_id` VARCHAR(20) UNIQUE NOT NULL DEFAULT '',
    `f_name` VARCHAR(20) NOT NULL,
    `l_name` VARCHAR(20) NOT NULL,
    `user_name` VARCHAR(20) UNIQUE NOT NULL,
    `email` VARCHAR(60) UNIQUE NOT NULL,
    `mobile` INT UNIQUE NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `join_date` DATE NOT NULL,
    `is_blocked` BOOLEAN NOT NULL DEFAULT FALSE,
    `verify` BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX (`trainer_id`),
    INDEX (`user_name`),
    INDEX (`email`),
    INDEX (`mobile`),
    INDEX (`join_date`)
);

-- Create the 'admin' table
CREATE TABLE IF NOT EXISTS `admin` (
    `admin_id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_name` VARCHAR(20) UNIQUE NOT NULL,
    `admin_email` VARCHAR(60) UNIQUE NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    INDEX (`admin_name`),
    INDEX (`admin_email`)
);

-- Create the 'topic' table
CREATE TABLE IF NOT EXISTS `topic` (
    `topic_id` INT AUTO_INCREMENT PRIMARY KEY,
    `topic_name` VARCHAR(50) NOT NULL,
    `created` DATE NOT NULL,
    `criteria` VARCHAR(100),
    `admin_id` INT,
    FOREIGN KEY (`admin_id`) REFERENCES `admin`(`admin_id`),
    INDEX (`topic_name`),
    INDEX (`created`)
);

-- Insert an admin record
INSERT INTO admin (admin_name, admin_email, password)
VALUES ('thush', 'thushanmadhusanka3@gmail.com', '67215bebe2fe2737d90bb951347c6a0852a1f537');
