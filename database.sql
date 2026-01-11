-- Restaurant Management System Database Schema

CREATE DATABASE IF NOT EXISTS restaurant_management;
USE restaurant_management;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('manager', 'staff') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food categories table
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
);

-- Food items table
CREATE TABLE IF NOT EXISTS food_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category_id INT,
    price DECIMAL(10, 2) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('cash', 'card', 'online') NOT NULL,
    payment_status ENUM('pending', 'completed') DEFAULT 'pending',
    FOREIGN KEY (staff_id) REFERENCES users(user_id)
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT NOT NULL,
    item_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES food_items(item_id)
);

-- Insert default categories
INSERT INTO categories (category_name) VALUES 
('Appetizers'),
('Main Course'),
('Desserts'),
('Beverages'),
('Salads');

-- Insert default admin user (password: admin123)
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'manager'),
('staff1', 'staff123', 'staff');

-- Insert sample food items
INSERT INTO food_items (item_name, category_id, price, availability) VALUES 
('Spring Rolls', 1, 5.99, TRUE),
('Chicken Wings', 1, 7.99, TRUE),
('Grilled Chicken', 2, 12.99, TRUE),
('Beef Steak', 2, 18.99, TRUE),
('Pasta Carbonara', 2, 11.99, TRUE),
('Chocolate Cake', 3, 6.99, TRUE),
('Ice Cream', 3, 4.99, TRUE),
('Coca Cola', 4, 2.99, TRUE),
('Fresh Juice', 4, 3.99, TRUE),
('Caesar Salad', 5, 8.99, TRUE);