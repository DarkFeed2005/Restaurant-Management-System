import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class DatabaseManager:
    """Handles all database operations"""
    
    @staticmethod
    def get_connection():
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='restaurant_management'
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        conn = DatabaseManager.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            else:
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except mysql.connector.Error as err:
            messagebox.showerror("Query Error", f"Error: {err}")
            if conn:
                conn.close()
            return None


class LoginWindow:
    """Login screen for authentication"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System - Login")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")
        
        # Center window
        self.center_window()
        
        # Main frame
        main_frame = tk.Frame(root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="Restaurant Management System", 
                        font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        subtitle = tk.Label(main_frame, text="Please login to continue", 
                           font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
        subtitle.pack(pady=10)
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg="#34495e", bd=2, relief="raised")
        form_frame.pack(pady=30, padx=20, fill="both", expand=True)
        
        # Username
        tk.Label(form_frame, text="Username:", font=("Arial", 11), 
                bg="#34495e", fg="white").pack(pady=(20, 5))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(form_frame, text="Password:", font=("Arial", 11), 
                bg="#34495e", fg="white").pack(pady=(15, 5))
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), 
                                      show="*", width=25)
        self.password_entry.pack(pady=5)
        
        # Login button
        login_btn = tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"),
                             bg="#27ae60", fg="white", width=20, height=2,
                             cursor="hand2", command=self.login)
        login_btn.pack(pady=30)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check credentials
        query = "SELECT user_id, role FROM users WHERE username = %s AND password = %s"
        result = DatabaseManager.execute_query(query, (username, password), fetch=True)
        
        if result:
            user_id, role = result[0]
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.root.destroy()
            
            # Open appropriate dashboard
            main_root = tk.Tk()
            if role == 'manager':
                ManagerDashboard(main_root, user_id, username)
            else:
                StaffDashboard(main_root, user_id, username)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")


class ManagerDashboard:
    """Manager dashboard with full system access"""
    
    def __init__(self, root, user_id, username):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.root.title("Manager Dashboard - Restaurant Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Header
        header = tk.Frame(root, bg="#2c3e50", height=80)
        header.pack(fill="x")
        
        tk.Label(header, text="Manager Dashboard", font=("Arial", 24, "bold"),
                bg="#2c3e50", fg="white").pack(side="left", padx=20, pady=15)
        
        tk.Label(header, text=f"Welcome, {username}", font=("Arial", 12),
                bg="#2c3e50", fg="#ecf0f1").pack(side="right", padx=20)
        
        logout_btn = tk.Button(header, text="Logout", font=("Arial", 10),
                              bg="#e74c3c", fg="white", command=self.logout)
        logout_btn.pack(side="right", padx=10)
        
        # Main container
        container = tk.Frame(root, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sidebar
        sidebar = tk.Frame(container, bg="#34495e", width=200)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        
        # Menu buttons
        buttons = [
            ("View Menu", self.show_menu),
            ("Manage Menu", self.manage_menu),
            ("View Orders", self.view_orders),
            ("Reports", self.show_reports),
            ("Search", self.search_function)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 11),
                          bg="#2c3e50", fg="white", width=18, height=2,
                          cursor="hand2", command=command, relief="flat")
            btn.pack(pady=5, padx=10)
        
        # Content area
        self.content_frame = tk.Frame(container, bg="white", relief="raised", bd=2)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Show default view
        self.show_menu()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_menu(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Restaurant Menu", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.content_frame, bg="white")
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), 
                bg="white").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        search_entry.pack(side="left", padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        columns = ("ID", "Name", "Category", "Price", "Available")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        # Load menu items
        query = """
            SELECT f.item_id, f.item_name, c.category_name, f.price, f.availability
            FROM food_items f
            LEFT JOIN categories c ON f.category_id = c.category_id
            ORDER BY c.category_name, f.item_name
        """
        items = DatabaseManager.execute_query(query, fetch=True)
        
        if items:
            for item in items:
                available = "Yes" if item[4] else "No"
                tree.insert("", "end", values=(item[0], item[1], item[2], 
                                              f"Rs. {item[3]:.2f}", available))
    
    def manage_menu(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Manage Menu Items", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.content_frame, bg="white")
        form_frame.pack(pady=20, padx=40, fill="x")
        
        # Item Name
        tk.Label(form_frame, text="Item Name:", font=("Arial", 11), 
                bg="white").grid(row=0, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Category
        tk.Label(form_frame, text="Category:", font=("Arial", 11), 
                bg="white").grid(row=1, column=0, sticky="w", pady=10)
        
        categories = DatabaseManager.execute_query(
            "SELECT category_id, category_name FROM categories", fetch=True)
        category_dict = {cat[1]: cat[0] for cat in categories}
        
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=category_var,
                                     values=list(category_dict.keys()),
                                     font=("Arial", 11), width=28, state="readonly")
        category_combo.grid(row=1, column=1, pady=10, padx=10)
        
        # Price
        tk.Label(form_frame, text="Price (Rs.):", font=("Arial", 11), 
                bg="white").grid(row=2, column=0, sticky="w", pady=10)
        price_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        price_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Availability
        availability_var = tk.BooleanVar(value=True)
        tk.Checkbutton(form_frame, text="Available", variable=availability_var,
                      font=("Arial", 11), bg="white").grid(row=3, column=1, 
                                                           sticky="w", pady=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def add_item():
            name = name_entry.get().strip()
            category = category_var.get()
            price = price_entry.get().strip()
            
            if not name or not category or not price:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            try:
                price_val = float(price)
                if price_val < 0:
                    raise ValueError()
            except:
                messagebox.showerror("Error", "Invalid price")
                return
            
            category_id = category_dict[category]
            query = """INSERT INTO food_items (item_name, category_id, price, availability)
                      VALUES (%s, %s, %s, %s)"""
            
            if DatabaseManager.execute_query(query, (name, category_id, price_val, 
                                                     availability_var.get())):
                messagebox.showinfo("Success", "Item added successfully!")
                name_entry.delete(0, "end")
                price_entry.delete(0, "end")
                category_var.set("")
                self.refresh_item_list(tree)
        
        tk.Button(btn_frame, text="Add Item", font=("Arial", 11, "bold"),
                 bg="#27ae60", fg="white", width=15, command=add_item).pack(side="left", padx=5)
        
        # Items list
        tk.Label(self.content_frame, text="Current Menu Items", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        list_frame = tk.Frame(self.content_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("ID", "Name", "Category", "Price", "Available")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        self.refresh_item_list(tree)
        
        # Delete button
        def delete_item():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select an item to delete")
                return
            
            item_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Confirm", "Delete this item?"):
                if DatabaseManager.execute_query("DELETE FROM food_items WHERE item_id = %s", 
                                                 (item_id,)):
                    messagebox.showinfo("Success", "Item deleted!")
                    self.refresh_item_list(tree)
        
        tk.Button(self.content_frame, text="Delete Selected Item", 
                 font=("Arial", 11), bg="#e74c3c", fg="white", 
                 command=delete_item).pack(pady=10)
    
    def refresh_item_list(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        query = """
            SELECT f.item_id, f.item_name, c.category_name, f.price, f.availability
            FROM food_items f
            LEFT JOIN categories c ON f.category_id = c.category_id
            ORDER BY c.category_name, f.item_name
        """
        items = DatabaseManager.execute_query(query, fetch=True)
        
        if items:
            for item in items:
                available = "Yes" if item[4] else "No"
                tree.insert("", "end", values=(item[0], item[1], item[2], 
                                              f"Rs. {item[3]:.2f}", available))
    
    def view_orders(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Order History", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        # Filter frame
        filter_frame = tk.Frame(self.content_frame, bg="white")
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Filter by Date:", font=("Arial", 10), 
                bg="white").pack(side="left", padx=5)
        
        date_var = tk.StringVar(value="All")
        date_combo = ttk.Combobox(filter_frame, textvariable=date_var,
                                 values=["All", "Today", "Last 7 Days", "Last 30 Days"],
                                 font=("Arial", 10), width=15, state="readonly")
        date_combo.pack(side="left", padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("Order ID", "Staff", "Date", "Items", "Total", "Payment", "Status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        
        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        def load_orders():
            for item in tree.get_children():
                tree.delete(item)
            
            query = """
                SELECT o.order_id, u.username, o.order_date, 
                       COUNT(oi.order_item_id), o.total_amount, 
                       o.payment_method, o.payment_status
                FROM orders o
                LEFT JOIN users u ON o.staff_id = u.user_id
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                GROUP BY o.order_id
                ORDER BY o.order_date DESC
            """
            orders = DatabaseManager.execute_query(query, fetch=True)
            
            if orders:
                for order in orders:
                    tree.insert("", "end", values=(
                        order[0], order[1], 
                        order[2].strftime("%Y-%m-%d %H:%M"),
                        order[3], f"Rs. {order[4]:.2f}", 
                        order[5].capitalize(), order[6].capitalize()
                    ))
        
        load_orders()
        
        tk.Button(filter_frame, text="Refresh", font=("Arial", 10),
                 bg="#3498db", fg="white", command=load_orders).pack(side="left", padx=5)
    
    def show_reports(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Sales Reports", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        # Report summary frame
        summary_frame = tk.Frame(self.content_frame, bg="white")
        summary_frame.pack(pady=20, padx=40, fill="x")
        
        # Get daily sales
        query = """
            SELECT DATE(order_date), COUNT(*), SUM(total_amount)
            FROM orders
            WHERE payment_status = 'completed' AND DATE(order_date) = CURDATE()
            GROUP BY DATE(order_date)
        """
        today_sales = DatabaseManager.execute_query(query, fetch=True)
        
        today_orders = today_sales[0][1] if today_sales else 0
        today_amount = today_sales[0][2] if today_sales else 0
        
        # Summary cards
        cards_frame = tk.Frame(summary_frame, bg="white")
        cards_frame.pack(pady=10)
        
        # Today's Sales Card
        card1 = tk.Frame(cards_frame, bg="#3498db", relief="raised", bd=3)
        card1.pack(side="left", padx=10, ipadx=20, ipady=20)
        
        tk.Label(card1, text="Today's Sales", font=("Arial", 12, "bold"),
                bg="#3498db", fg="white").pack()
        tk.Label(card1, text=f"Rs. {today_amount:.2f}", font=("Arial", 18, "bold"),
                bg="#3498db", fg="white").pack()
        tk.Label(card1, text=f"{today_orders} Orders", font=("Arial", 10),
                bg="#3498db", fg="white").pack()
        
        # Total Orders Card
        total_orders = DatabaseManager.execute_query(
            "SELECT COUNT(*) FROM orders WHERE payment_status = 'completed'", fetch=True)
        
        card2 = tk.Frame(cards_frame, bg="#27ae60", relief="raised", bd=3)
        card2.pack(side="left", padx=10, ipadx=20, ipady=20)
        
        tk.Label(card2, text="Total Orders", font=("Arial", 12, "bold"),
                bg="#27ae60", fg="white").pack()
        tk.Label(card2, text=f"{total_orders[0][0] if total_orders else 0}", 
                font=("Arial", 18, "bold"), bg="#27ae60", fg="white").pack()
        tk.Label(card2, text="All Time", font=("Arial", 10),
                bg="#27ae60", fg="white").pack()
        
        # Top selling items
        tk.Label(self.content_frame, text="Top Selling Items", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        
        table_frame = tk.Frame(self.content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        columns = ("Item Name", "Quantity Sold", "Revenue")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")
        
        tree.pack(fill="both", expand=True)
        
        query = """
            SELECT f.item_name, SUM(oi.quantity), SUM(oi.subtotal)
            FROM order_items oi
            JOIN food_items f ON oi.item_id = f.item_id
            GROUP BY f.item_id, f.item_name
            ORDER BY SUM(oi.quantity) DESC
            LIMIT 10
        """
        items = DatabaseManager.execute_query(query, fetch=True)
        
        if items:
            for item in items:
                tree.insert("", "end", values=(item[0], item[1], f"Rs. {item[2]:.2f}"))
    
    def search_function(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Search", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        search_frame = tk.Frame(self.content_frame, bg="white")
        search_frame.pack(pady=20)
        
        tk.Label(search_frame, text="Search in:", font=("Arial", 11), 
                bg="white").pack(side="left", padx=5)
        
        search_type = tk.StringVar(value="Menu")
        ttk.Combobox(search_frame, textvariable=search_type,
                    values=["Menu", "Orders"], font=("Arial", 11),
                    width=15, state="readonly").pack(side="left", padx=5)
        
        tk.Label(search_frame, text="Keyword:", font=("Arial", 11), 
                bg="white").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        search_entry.pack(side="left", padx=5)
        
        result_frame = tk.Frame(self.content_frame, bg="white")
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        def perform_search():
            for widget in result_frame.winfo_children():
                widget.destroy()
            
            keyword = search_entry.get().strip()
            if not keyword:
                messagebox.showerror("Error", "Please enter a search keyword")
                return
            
            if search_type.get() == "Menu":
                query = """
                    SELECT f.item_name, c.category_name, f.price, f.availability
                    FROM food_items f
                    LEFT JOIN categories c ON f.category_id = c.category_id
                    WHERE f.item_name LIKE %s
                """
                results = DatabaseManager.execute_query(query, (f"%{keyword}%",), fetch=True)
                
                columns = ("Name", "Category", "Price", "Available")
                tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=15)
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=200, anchor="center")
                
                tree.pack(fill="both", expand=True)
                
                if results:
                    for item in results:
                        available = "Yes" if item[3] else "No"
                        tree.insert("", "end", values=(item[0], item[1], 
                                                      f"Rs. {item[2]:.2f}", available))
                else:
                    tk.Label(result_frame, text="No results found", 
                            font=("Arial", 12), bg="white").pack(pady=20)
        
        tk.Button(search_frame, text="Search", font=("Arial", 11),
                 bg="#3498db", fg="white", command=perform_search).pack(side="left", padx=5)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()


class StaffDashboard:
    """Staff dashboard for order management"""
    
    def __init__(self, root, user_id, username):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.current_order = []
        
        self.root.title("Staff Dashboard - Restaurant Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Header
        header = tk.Frame(root, bg="#16a085", height=80)
        header.pack(fill="x")
        
        tk.Label(header, text="Staff Dashboard", font=("Arial", 24, "bold"),
                bg="#16a085", fg="white").pack(side="left", padx=20, pady=15)
        
        tk.Label(header, text=f"Welcome, {username}", font=("Arial", 12),
                bg="#16a085", fg="white").pack(side="right", padx=20)
        
        logout_btn = tk.Button(header, text="Logout", font=("Arial", 10),
                              bg="#c0392b", fg="white", command=self.logout)
        logout_btn.pack(side="right", padx=10)
        
        # Main container
        container = tk.Frame(root, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sidebar
        sidebar = tk.Frame(container, bg="#1abc9c", width=200)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        
        buttons = [
            ("Take Order", self.take_order),
            ("View Menu", self.view_menu),
            ("Order History", self.order_history)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 11),
                          bg="#16a085", fg="white", width=18, height=2,
                          cursor="hand2", command=command, relief="flat")
            btn.pack(pady=5, padx=10)
        
        # Content area
        self.content_frame = tk.Frame(container, bg="white", relief="raised", bd=2)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Show default view
        self.take_order()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def view_menu(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Menu", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        table_frame = tk.Frame(self.content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("Name", "Category", "Price", "Available")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, height=25)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")
        
        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        query = """
            SELECT f.item_name, c.category_name, f.price, f.availability
            FROM food_items f
            LEFT JOIN categories c ON f.category_id = c.category_id
            WHERE f.availability = TRUE
            ORDER BY c.category_name, f.item_name
        """
        items = DatabaseManager.execute_query(query, fetch=True)
        
        if items:
            for item in items:
                available = "Yes" if item[3] else "No"
                tree.insert("", "end", values=(item[0], item[1], 
                                              f"Rs. {item[2]:.2f}", available))
    
    def take_order(self):
        self.clear_content()
        self.current_order = []
        
        tk.Label(self.content_frame, text="Take New Order", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        # Split into two columns
        main_container = tk.Frame(self.content_frame, bg="white")
        main_container.pack(fill="both", expand=True, padx=20)
        
        # Left side - Menu items
        left_frame = tk.Frame(main_container, bg="white")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="Available Items", font=("Arial", 14, "bold"),
                bg="white").pack(pady=10)
        
        # Menu list
        menu_frame = tk.Frame(left_frame, bg="white")
        menu_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(menu_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("ID", "Name", "Price")
        self.menu_tree = ttk.Treeview(menu_frame, columns=columns, show="headings",
                                      yscrollcommand=scrollbar.set, height=20)
        
        for col in columns:
            self.menu_tree.heading(col, text=col)
        
        self.menu_tree.column("ID", width=50, anchor="center")
        self.menu_tree.column("Name", width=200)
        self.menu_tree.column("Price", width=100, anchor="center")
        
        self.menu_tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.menu_tree.yview)
        
        # Load menu
        self.load_menu_items()
        
        # Add to order section
        add_frame = tk.Frame(left_frame, bg="white")
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="Quantity:", font=("Arial", 10),
                bg="white").pack(side="left", padx=5)
        qty_entry = tk.Entry(add_frame, font=("Arial", 10), width=10)
        qty_entry.insert(0, "1")
        qty_entry.pack(side="left", padx=5)
        
        def add_to_order():
            selected = self.menu_tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select an item")
                return
            
            try:
                qty = int(qty_entry.get())
                if qty <= 0:
                    raise ValueError()
            except:
                messagebox.showerror("Error", "Invalid quantity")
                return
            
            item = self.menu_tree.item(selected[0])['values']
            item_id = item[0]
            item_name = item[1]
            price = float(item[2].replace("Rs. ", ""))
            
            # Add to current order
            self.current_order.append({
                'id': item_id,
                'name': item_name,
                'price': price,
                'quantity': qty,
                'subtotal': price * qty
            })
            
            self.update_order_list()
            qty_entry.delete(0, "end")
            qty_entry.insert(0, "1")
        
        tk.Button(add_frame, text="Add to Order", font=("Arial", 10, "bold"),
                 bg="#27ae60", fg="white", command=add_to_order).pack(side="left", padx=5)
        
        # Right side - Current order
        right_frame = tk.Frame(main_container, bg="#ecf0f1", relief="raised", bd=2)
        right_frame.pack(side="right", fill="both", expand=True)
        
        tk.Label(right_frame, text="Current Order", font=("Arial", 14, "bold"),
                bg="#ecf0f1").pack(pady=10)
        
        # Order list
        order_frame = tk.Frame(right_frame, bg="white")
        order_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        order_scrollbar = tk.Scrollbar(order_frame)
        order_scrollbar.pack(side="right", fill="y")
        
        order_cols = ("Item", "Qty", "Price", "Subtotal")
        self.order_tree = ttk.Treeview(order_frame, columns=order_cols, show="headings",
                                       yscrollcommand=order_scrollbar.set, height=15)
        
        for col in order_cols:
            self.order_tree.heading(col, text=col)
        
        self.order_tree.column("Item", width=150)
        self.order_tree.column("Qty", width=50, anchor="center")
        self.order_tree.column("Price", width=80, anchor="center")
        self.order_tree.column("Subtotal", width=80, anchor="center")
        
        self.order_tree.pack(fill="both", expand=True)
        order_scrollbar.config(command=self.order_tree.yview)
        
        # Remove item button
        tk.Button(right_frame, text="Remove Selected", font=("Arial", 10),
                 bg="#e74c3c", fg="white", command=self.remove_from_order).pack(pady=5)
        
        # Total
        self.total_label = tk.Label(right_frame, text="Total: Rs. 0.00", 
                                    font=("Arial", 16, "bold"), bg="#ecf0f1")
        self.total_label.pack(pady=10)
        
        # Payment method
        payment_frame = tk.Frame(right_frame, bg="#ecf0f1")
        payment_frame.pack(pady=10)
        
        tk.Label(payment_frame, text="Payment:", font=("Arial", 11),
                bg="#ecf0f1").pack(side="left", padx=5)
        
        self.payment_var = tk.StringVar(value="cash")
        for method in ["cash", "card", "online"]:
            tk.Radiobutton(payment_frame, text=method.capitalize(), 
                          variable=self.payment_var, value=method,
                          font=("Arial", 10), bg="#ecf0f1").pack(side="left", padx=5)
        
        # Submit order
        tk.Button(right_frame, text="Submit Order", font=("Arial", 12, "bold"),
                 bg="#3498db", fg="white", width=20, height=2,
                 command=self.submit_order).pack(pady=10)
        
        tk.Button(right_frame, text="Clear Order", font=("Arial", 10),
                 bg="#95a5a6", fg="white", command=self.clear_order).pack(pady=5)
    
    def load_menu_items(self):
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        
        query = """
            SELECT item_id, item_name, price
            FROM food_items
            WHERE availability = TRUE
            ORDER BY item_name
        """
        items = DatabaseManager.execute_query(query, fetch=True)
        
        if items:
            for item in items:
                self.menu_tree.insert("", "end", values=(item[0], item[1], 
                                                        f"Rs. {item[2]:.2f}"))
    
    def update_order_list(self):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        total = 0
        for item in self.current_order:
            self.order_tree.insert("", "end", values=(
                item['name'], item['quantity'],
                f"Rs. {item['price']:.2f}",
                f"Rs. {item['subtotal']:.2f}"
            ))
            total += item['subtotal']
        
        self.total_label.config(text=f"Total: Rs. {total:.2f}")
    
    def remove_from_order(self):
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to remove")
            return
        
        index = self.order_tree.index(selected[0])
        del self.current_order[index]
        self.update_order_list()
    
    def clear_order(self):
        if messagebox.askyesno("Confirm", "Clear current order?"):
            self.current_order = []
            self.update_order_list()
    
    def submit_order(self):
        if not self.current_order:
            messagebox.showerror("Error", "Order is empty")
            return
        
        total = sum(item['subtotal'] for item in self.current_order)
        payment_method = self.payment_var.get()
        
        # Insert order
        order_query = """
            INSERT INTO orders (staff_id, total_amount, payment_method, payment_status)
            VALUES (%s, %s, %s, 'completed')
        """
        
        conn = DatabaseManager.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(order_query, (self.user_id, total, payment_method))
            order_id = cursor.lastrowid
            
            # Insert order items
            item_query = """
                INSERT INTO order_items (order_id, item_id, quantity, item_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            for item in self.current_order:
                cursor.execute(item_query, (order_id, item['id'], item['quantity'],
                                           item['price'], item['subtotal']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", 
                              f"Order #{order_id} submitted successfully!\nTotal: Rs. {total:.2f}")
            self.current_order = []
            self.update_order_list()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to submit order: {err}")
            if conn:
                conn.close()
    
    def order_history(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="My Order History", 
                font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        
        table_frame = tk.Frame(self.content_frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("Order ID", "Date", "Items", "Total", "Payment")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, height=25)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="center")
        
        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        query = """
            SELECT o.order_id, o.order_date, COUNT(oi.order_item_id), 
                   o.total_amount, o.payment_method
            FROM orders o
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.staff_id = %s
            GROUP BY o.order_id
            ORDER BY o.order_date DESC
        """
        orders = DatabaseManager.execute_query(query, (self.user_id,), fetch=True)
        
        if orders:
            for order in orders:
                tree.insert("", "end", values=(
                    order[0],
                    order[1].strftime("%Y-%m-%d %H:%M"),
                    order[2],
                    f"Rs. {order[3]:.2f}",
                    order[4].capitalize()
                ))
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()