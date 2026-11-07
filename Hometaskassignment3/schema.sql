CREATE DATABASE IF NOT EXISTS waste_management;

USE waste_management;

CREATE TABLE IF NOT EXISTS waste_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    material VARCHAR(50) NOT NULL,
    disposal_method VARCHAR(150) NOT NULL
);

INSERT INTO waste_items (item_name, material, disposal_method)
VALUES
('Glass Jar', 'Glass', 'Glass recycling container'),
('Plastic Bottle', 'Plastic', 'Plastic recycling bin'),
('Newspaper', 'Paper', 'Paper recycling bin'),
('Food Can', 'Metal', 'Metal recycling container'),
('Cardboard Box', 'Paper', 'Paper recycling bin');