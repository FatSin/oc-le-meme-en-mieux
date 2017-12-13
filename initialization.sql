CREATE DATABASE openfood CHARACTER SET 'utf8';
USE openfood;

CREATE TABLE IF NOT EXISTS Categories (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(40) UNIQUE NOT NULL
)
ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS Products (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(40) UNIQUE NOT NULL,
	CategoryName VARCHAR(40) NOT NULL,
    Places VARCHAR(40),
    Stores VARCHAR(40),
	Grade VARCHAR(1) NOT NULL,
	Link VARCHAR(100)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Substitutes (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(40) NOT NULL,
    SubName VARCHAR(40) NOT NULL,
    Places VARCHAR(40),
    Stores VARCHAR(40),
	Link VARCHAR(100)
)
ENGINE=InnoDB;




