CREATE DATABASE analytics_db;
USE analytics_db;

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    quantity INT,
    price FLOAT,
    sale_date DATE
);

INSERT INTO sales (product_name, quantity, price, sale_date)
VALUES
('Laptop', 2, 50000, '2025-09-01'),
('Mobile', 5, 15000, '2025-09-02'),
('Tablet', 3, 20000, '2025-09-03');