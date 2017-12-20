-- MySQL Script generated by MySQL Workbench
-- 12/16/17 11:03:48
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema openfoodfacts_oc
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `openfoodfacts_oc` ;

-- -----------------------------------------------------
-- Schema openfoodfacts_oc
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `openfoodfacts_oc` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `openfoodfacts_oc` ;

-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`Categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`Categories` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`Categories` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`Products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`Products` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`Products` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` BIGINT(20) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `cat_id` INT UNSIGNED NOT NULL,
  `nutri_grade` CHAR(1) NULL,
  `energy` INT NULL,
  `fat` FLOAT NULL,
  `carbs` FLOAT NULL,
  `fibers` FLOAT NULL,
  `sugars` FLOAT NULL,
  `proteins` FLOAT NULL,
  `salt` FLOAT NULL,
  `url` VARCHAR(1000) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_Products_Categories_idx` (`cat_id` ASC),
  CONSTRAINT `fk_cat_id`
    FOREIGN KEY (`cat_id`)
    REFERENCES `openfoodfacts_oc`.`Categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`Favorites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`Favorites` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`Favorites` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_id` INT UNSIGNED NOT NULL,
  `substitute_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_Favorites_Products1_idx` (`product_id` ASC),
  INDEX `fk_Favorites_Products2_idx` (`substitute_id` ASC),
  CONSTRAINT `fk_Favorites_Products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `openfoodfacts_oc`.`Products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Favorites_Products2`
    FOREIGN KEY (`substitute_id`)
    REFERENCES `openfoodfacts_oc`.`Products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`Stores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`Stores` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`Stores` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`Brands`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`Brands` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`Brands` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`ProductsBrands`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`ProductsBrands` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`ProductsBrands` (
  `Brands_id` INT UNSIGNED NOT NULL,
  `Products_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`Brands_id`, `Products_id`),
  INDEX `fk_ProductsBrands_Brands1_idx` (`Brands_id` ASC),
  INDEX `fk_ProductsBrands_Products1_idx` (`Products_id` ASC),
  CONSTRAINT `fk_ProductsBrands_Brands1`
    FOREIGN KEY (`Brands_id`)
    REFERENCES `openfoodfacts_oc`.`Brands` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ProductsBrands_Products1`
    FOREIGN KEY (`Products_id`)
    REFERENCES `openfoodfacts_oc`.`Products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `openfoodfacts_oc`.`ProductsStores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `openfoodfacts_oc`.`ProductsStores` ;

CREATE TABLE IF NOT EXISTS `openfoodfacts_oc`.`ProductsStores` (
  `Products_id` INT UNSIGNED NOT NULL,
  `Stores_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`Products_id`, `Stores_id`),
  INDEX `fk_ProductsStores_Products1_idx` (`Products_id` ASC),
  INDEX `fk_ProductsStores_Stores1_idx` (`Stores_id` ASC),
  CONSTRAINT `fk_ProductsStores_Products1`
    FOREIGN KEY (`Products_id`)
    REFERENCES `openfoodfacts_oc`.`Products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ProductsStores_Stores1`
    FOREIGN KEY (`Stores_id`)
    REFERENCES `openfoodfacts_oc`.`Stores` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;