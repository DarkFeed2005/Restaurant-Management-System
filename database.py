import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''  # Change to your MySQL password
        self.database = 'restaurant_management'
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(buffered=True)
            return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
            
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            self.connect()
            query = "SELECT user_id, username, role FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            self.close()
            return user
        except Error as e:
            print(f"Authentication error: {e}")
            self.close()
            return None
            
    def get_all_food_items(self):
        """Get all food items with category names"""
        try:
            self.connect()
            query = """
                SELECT f.item_id, f.item_name, c.category_name, f.price, f.availability 
                FROM food_items f
                LEFT JOIN categories c ON f.category_id = c.category_id
                ORDER BY c.category_name, f.item_name
            """
            self.cursor.execute(query)
            items = self.cursor.fetchall()
            self.close()
            return items
        except Error as e:
            print(f"Error fetching food items: {e}")
            self.close()
            return []
            
    def get_categories(self):
        """Get all categories"""
        try:
            self.connect()
            query = "SELECT category_id, category_name FROM categories"
            self.cursor.execute(query)
            categories = self.cursor.fetchall()
            self.close()
            return categories
        except Error as e:
            print(f"Error fetching categories: {e}")
            self.close()
            return []
            
    def add_food_item(self, name, category_id, price, availability=1):
        """Add new food item"""
        try:
            self.connect()
            query = "INSERT INTO food_items (item_name, category_id, price, availability) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (name, category_id, price, availability))
            self.conn.commit()
            item_id = self.cursor.lastrowid
            self.close()
            return item_id
        except Error as e:
            print(f"Error adding food item: {e}")
            self.close()
            return None
            
    def update_food_item(self, item_id, name, category_id, price, availability):
        """Update existing food item"""
        try:
            self.connect()
            query = "UPDATE food_items SET item_name=%s, category_id=%s, price=%s, availability=%s WHERE item_id=%s"
            self.cursor.execute(query, (name, category_id, price, availability, item_id))
            self.conn.commit()
            self.close()
            return True
        except Error as e:
            print(f"Error updating food item: {e}")
            self.close()
            return False
            
    def delete_food_item(self, item_id):
        """Delete food item"""
        try:
            self.connect()
            query = "DELETE FROM food_items WHERE item_id=%s"
            self.cursor.execute(query, (item_id,))
            self.conn.commit()
            self.close()
            return True
        except Error as e:
            print(f"Error deleting food item: {e}")
            self.close()
            return False
            
    def create_order(self, staff_id, items, payment_method):
        """Create new order with items"""
        try:
            self.connect()
            
            # Calculate total
            total = sum(item['price'] * item['quantity'] for item in items)
            
            # Insert order
            order_query = "INSERT INTO orders (staff_id, total_amount, payment_method, payment_status) VALUES (%s, %s, %s, 'completed')"
            self.cursor.execute(order_query, (staff_id, total, payment_method))
            order_id = self.cursor.lastrowid
            
            # Insert order items
            for item in items:
                item_query = "INSERT INTO order_items (order_id, item_id, quantity, item_price, subtotal) VALUES (%s, %s, %s, %s, %s)"
                subtotal = item['price'] * item['quantity']
                self.cursor.execute(item_query, (order_id, item['item_id'], item['quantity'], item['price'], subtotal))
            
            self.conn.commit()
            self.close()
            return order_id
        except Error as e:
            print(f"Error creating order: {e}")
            if self.conn:
                self.conn.rollback()
            self.close()
            return None
            
    def get_order_history(self, staff_id=None):
        """Get order history (filtered by staff if provided)"""
        try:
            self.connect()
            if staff_id:
                query = """
                    SELECT o.order_id, o.order_date, o.total_amount, o.payment_method, 
                           u.username, o.payment_status
                    FROM orders o
                    JOIN users u ON o.staff_id = u.user_id
                    WHERE o.staff_id = %s
                    ORDER BY o.order_date DESC
                """
                self.cursor.execute(query, (staff_id,))
            else:
                query = """
                    SELECT o.order_id, o.order_date, o.total_amount, o.payment_method, 
                           u.username, o.payment_status
                    FROM orders o
                    JOIN users u ON o.staff_id = u.user_id
                    ORDER BY o.order_date DESC
                """
                self.cursor.execute(query)
            
            orders = self.cursor.fetchall()
            self.close()
            return orders
        except Error as e:
            print(f"Error fetching order history: {e}")
            self.close()
            return []
            
    def get_order_details(self, order_id):
        """Get detailed items for a specific order"""
        try:
            self.connect()
            query = """
                SELECT f.item_name, oi.quantity, oi.item_price, oi.subtotal
                FROM order_items oi
                JOIN food_items f ON oi.item_id = f.item_id
                WHERE oi.order_id = %s
            """
            self.cursor.execute(query, (order_id,))
            items = self.cursor.fetchall()
            self.close()
            return items
        except Error as e:
            print(f"Error fetching order details: {e}")
            self.close()
            return []
            
    def get_daily_sales(self, date=None):
        """Get daily sales report"""
        try:
            self.connect()
            if date:
                query = """
                    SELECT DATE(order_date) as date, COUNT(*) as orders, SUM(total_amount) as total
                    FROM orders
                    WHERE DATE(order_date) = %s AND payment_status = 'completed'
                    GROUP BY DATE(order_date)
                """
                self.cursor.execute(query, (date,))
            else:
                query = """
                    SELECT DATE(order_date) as date, COUNT(*) as orders, SUM(total_amount) as total
                    FROM orders
                    WHERE payment_status = 'completed'
                    GROUP BY DATE(order_date)
                    ORDER BY date DESC
                    LIMIT 10
                """
                self.cursor.execute(query)
            
            sales = self.cursor.fetchall()
            self.close()
            return sales
        except Error as e:
            print(f"Error fetching daily sales: {e}")
            self.close()
            return []
            
    def get_top_selling_items(self, limit=10):
        """Get top selling food items"""
        try:
            self.connect()
            query = """
                SELECT f.item_name, SUM(oi.quantity) as total_quantity, 
                       SUM(oi.subtotal) as total_revenue
                FROM order_items oi
                JOIN food_items f ON oi.item_id = f.item_id
                GROUP BY f.item_id, f.item_name
                ORDER BY total_quantity DESC
                LIMIT %s
            """
            self.cursor.execute(query, (limit,))
            items = self.cursor.fetchall()
            self.close()
            return items
        except Error as e:
            print(f"Error fetching top selling items: {e}")
            self.close()
            return []
            
    def search_food_items(self, search_term):
        """Search food items by name"""
        try:
            self.connect()
            query = """
                SELECT f.item_id, f.item_name, c.category_name, f.price, f.availability 
                FROM food_items f
                LEFT JOIN categories c ON f.category_id = c.category_id
                WHERE f.item_name LIKE %s
                ORDER BY f.item_name
            """
            self.cursor.execute(query, (f'%{search_term}%',))
            items = self.cursor.fetchall()
            self.close()
            return items
        except Error as e:
            print(f"Error searching food items: {e}")
            self.close()
            return []