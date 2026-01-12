-- Restaurant Management System Database Schema
-- Created: 2025
-- Database: MySQL

-- Create database
CREATE DATABASE IF NOT EXISTS restaurant_management;
USE restaurant_management;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS food_items;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('manager', 'staff') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Food categories table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Food items table
CREATE TABLE food_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category_id INT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
    INDEX idx_category (category_id),
    INDEX idx_availability (availability)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Orders table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    payment_method ENUM('cash', 'card', 'online') NOT NULL,
    payment_status ENUM('pending', 'completed') DEFAULT 'pending',
    FOREIGN KEY (staff_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_staff (staff_id),
    INDEX idx_order_date (order_date),
    INDEX idx_payment_status (payment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Order items table
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    item_price DECIMAL(10, 2) NOT NULL CHECK (item_price >= 0),
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES food_items(item_id) ON DELETE SET NULL,
    INDEX idx_order (order_id),
    INDEX idx_item (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert default categories
INSERT INTO categories (category_name) VALUES 
('Appetizers'),
('Main Course'),
('Desserts'),
('Beverages'),
('Salads'),
('Fast Food'),
('Sri Lankan');

-- Insert default users
-- Password: admin123 for manager, staff123 for staff
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'manager'),
('staff1', 'staff123', 'staff'),
('staff2', 'staff123', 'staff');

-- Insert sample food items
INSERT INTO food_items (item_name, category_id, price, availability) VALUES 
-- Appetizers
('Spring Rolls', 1, 350.00, TRUE),
('Chicken Wings', 1, 450.00, TRUE),
('Garlic Bread', 1, 250.00, TRUE),

-- Main Course
('Grilled Chicken', 2, 850.00, TRUE),
('Beef Steak', 2, 1250.00, TRUE),
('Pasta Carbonara', 2, 750.00, TRUE),
('Fish & Chips', 2, 900.00, TRUE),

-- Sri Lankan
('Rice & Curry', 7, 350.00, TRUE),
('Fried Rice', 7, 400.00, TRUE),
('Kottu Roti', 7, 450.00, TRUE),
('String Hoppers', 7, 200.00, TRUE),

-- Fast Food
('Chicken Burger', 6, 500.00, TRUE),
('Beef Burger', 6, 550.00, TRUE),
('Pizza (Medium)', 6, 800.00, TRUE),
('Sandwich', 6, 350.00, TRUE),
('Hot Dog', 6, 300.00, TRUE),

-- Desserts
('Chocolate Cake', 3, 450.00, TRUE),
('Ice Cream', 3, 250.00, TRUE),
('Watalappan', 3, 200.00, TRUE),
('Brownie', 3, 350.00, TRUE),

-- Beverages
('Coca Cola', 4, 150.00, TRUE),
('Sprite', 4, 150.00, TRUE),
('Fresh Juice', 4, 250.00, TRUE),
('Coffee', 4, 200.00, TRUE),
('Tea', 4, 100.00, TRUE),
('Milkshake', 4, 300.00, TRUE),

-- Salads
('Caesar Salad', 5, 550.00, TRUE),
('Greek Salad', 5, 600.00, TRUE),
('Garden Salad', 5, 450.00, TRUE);

-- Insert sample orders (optional - for testing)
INSERT INTO orders (staff_id, total_amount, payment_method, payment_status, order_date) VALUES
(2, 1200.00, 'cash', 'completed', '2025-01-10 12:30:00'),
(2, 850.00, 'card', 'completed', '2025-01-10 13:15:00'),
(3, 1500.00, 'online', 'completed', '2025-01-11 11:45:00'),
(2, 950.00, 'cash', 'completed', '2025-01-11 14:20:00'),
(3, 2100.00, 'card', 'completed', '2025-01-12 10:30:00');

-- Insert sample order items for the orders above
INSERT INTO order_items (order_id, item_id, quantity, item_price, subtotal) VALUES
-- Order 1
(1, 8, 2, 350.00, 700.00),
(1, 14, 1, 500.00, 500.00),

-- Order 2
(2, 4, 1, 850.00, 850.00),

-- Order 3
(3, 5, 1, 1250.00, 1250.00),
(3, 17, 1, 250.00, 250.00),

-- Order 4
(4, 9, 1, 400.00, 400.00),
(4, 10, 1, 450.00, 450.00),
(4, 21, 1, 100.00, 100.00),

-- Order 5
(5, 15, 2, 800.00, 1600.00),
(5, 14, 1, 500.00, 500.00);

-- Create views for common queries

-- View for menu items with category names
CREATE OR REPLACE VIEW v_menu_items AS
SELECT 
    f.item_id,
    f.item_name,
    c.category_name,
    f.price,
    f.availability,
    f.created_at
FROM food_items f
LEFT JOIN categories c ON f.category_id = c.category_id;

-- View for order details
CREATE OR REPLACE VIEW v_order_details AS
SELECT 
    o.order_id,
    o.order_date,
    u.username AS staff_name,
    o.total_amount,
    o.payment_method,
    o.payment_status,
    COUNT(oi.order_item_id) AS item_count
FROM orders o
LEFT JOIN users u ON o.staff_id = u.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;

-- View for daily sales summary
CREATE OR REPLACE VIEW v_daily_sales AS
SELECT 
    DATE(order_date) AS sale_date,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_sales,
    AVG(total_amount) AS average_order
FROM orders
WHERE payment_status = 'completed'
GROUP BY DATE(order_date)
ORDER BY sale_date DESC;

-- Create stored procedures

-- Procedure to get top selling items
DELIMITER //
CREATE PROCEDURE sp_get_top_selling_items(IN limit_count INT)
BEGIN
    SELECT 
        f.item_name,
        SUM(oi.quantity) AS total_quantity,
        SUM(oi.subtotal) AS total_revenue
    FROM order_items oi
    JOIN food_items f ON oi.item_id = f.item_id
    GROUP BY f.item_id, f.item_name
    ORDER BY total_quantity DESC
    LIMIT limit_count;
END //
DELIMITER ;

-- Procedure to get staff performance
DELIMITER //
CREATE PROCEDURE sp_get_staff_performance()
BEGIN
    SELECT 
        u.username,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS total_sales,
        AVG(o.total_amount) AS average_sale
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.staff_id
    WHERE u.role = 'staff' AND o.payment_status = 'completed'
    GROUP BY u.user_id, u.username
    ORDER BY total_sales DESC;
END //
DELIMITER ;

-- Grant necessary permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON restaurant_management.* TO 'your_mysql_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Display table information
SELECT 'Database setup completed successfully!' AS Status;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS category_count FROM categories;
SELECT COUNT(*) AS food_item_count FROM food_items;
SELECT COUNT(*) AS order_count FROM orders;