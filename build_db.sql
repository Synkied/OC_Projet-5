DROP DATABASE IF EXISTS openfoodfacts_oc;
CREATE DATABASE openfoodfacts_oc;

USE openfoodfacts_oc;

CREATE TABLE Categories(
       id INT UNSIGNED NOT NULL AUTO INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       url VARCHAR(1000),
       num_products INT NOT NULL
)
ENGINE=InnoDB;


CREATE TABLE Products(
       id INT UNSIGNED NOT NULL AUTO INCREMENT PRIMARY KEY,
       category_id INT NOT NULL,
       name VARCHAR(150),
       brand VARCHAR(100),
       store VARCHAR(100),
       nutri_grade CHAR(1),
       energy INT,
       fat FLOAT,
       carbs FLOAT,
       fibers FLOAT,
       sugars FLOAT,
       proteins FLOAT,
       salt FLOAT,
       traces VARCHAR(150),
       CONSTRAINT fk_cat_id
              FOREIGN KEY (category_id)
              REFERENCES Categories(id)
)
ENGINE=InnoDB;


CREATE TABLE Stores(
       id INT UNSIGNED NOT NULL AUTO INCREMENT PRIMARY KEY,
       name VARCHAR(100) UNIQUE
)
ENGINE=InnoDB;


CREATE TABLE Brands(
       id INT UNSIGNED NOT NULL AUTO INCREMENT PRIMARY KEY,
       name VARCHAR(100) UNIQUE
)
ENGINE=InnoDB;


CREATE TABLE Favorites(
       id INT UNSIGNED NOT NULL AUTO INCREMENT PRIMARY KEY,
       product_id INT,
       substitute_id INT,
       CONSTRAINT fk_prod_id
              FOREIGN KEY (product_id)
              REFERENCES Products(id),
       CONSTRAINT fk_subst_id
              FOREIGN KEY (substitute_id)
              REFERENCES Products(id)
)
ENGINE=InnoDB;