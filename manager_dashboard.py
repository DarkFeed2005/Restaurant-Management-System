import customtkinter as ctk
from tkinter import messagebox, ttk
from db_connection import get_connection
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ManagerDashboard:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        
        self.window = ctk.CTk()
        self.window.title("Manager Dashboard")
        self.window.geometry("1400x800")
        
        # Center window
        self.window.update_idletasks()
        width = 1400
        height = 800
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.show_dashboard()
        self.window.mainloop()
    
    def show_dashboard(self):
        """Display main dashboard"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text="👨‍💼 Manager Dashboard",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            header,
            text=f"Welcome, {self.username}",
            font=ctk.CTkFont(size=16),
            text_color="#B0B0B0"
        ).pack(side="right", padx=30)
        
        # Main content
        content = ctk.CTkFrame(self.window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Button grid with icons and colors
        buttons = [
            ("🍽️ Manage Menu", self.manage_menu, '#1E88E5'),
            ("📋 View Orders", self.view_orders, '#43A047'),
            ("📊 Sales Reports", self.sales_reports, '#AB47BC'),
            ("👥 Manage Users", self.manage_users, '#FF7043'),
            ("📖 View Menu", self.view_menu, '#26A69A'),
            ("🚪 Logout", self.logout, '#EF5350')
        ]
        
        row, col = 0, 0
        for text, command, color in buttons:
            btn = ctk.CTkButton(
                content,
                text=text,
                font=ctk.CTkFont(size=20, weight="bold"),
                width=380,
                height=150,
                corner_radius=15,
                fg_color=color,
                hover_color=self.darken_color(color),
                command=command
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Configure grid
        for i in range(3):
            content.columnconfigure(i, weight=1)
        for i in range(2):
            content.rowconfigure(i, weight=1)
    
    def darken_color(self, color):
        """Darken a hex color"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def manage_menu(self):
        """Manage food items"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🍽️ Manage Menu",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="← Back",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#424242",
            hover_color="#616161",
            command=self.show_dashboard
        ).pack(side="right", padx=30)
        
        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Form
        left_panel = ctk.CTkFrame(main_container, width=420, corner_radius=15, fg_color="#1E1E1E")
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            left_panel,
            text="Food Item Details",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=20)
        
        # Item Name
        ctk.CTkLabel(left_panel, text="Item Name", font=ctk.CTkFont(size=14), 
                    text_color="#B0B0B0").pack(pady=(10, 5))
        self.item_name = ctk.CTkEntry(left_panel, width=350, height=40, 
                                     font=ctk.CTkFont(size=14), corner_radius=10)
        self.item_name.pack(pady=5)
        
        # Category
        ctk.CTkLabel(left_panel, text="Category", font=ctk.CTkFont(size=14),
                    text_color="#B0B0B0").pack(pady=(10, 5))
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT category_id, category_name FROM categories")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        
        self.category_var = ctk.StringVar()
        self.category_dict = {name: id for id, name in categories}
        category_combo = ctk.CTkComboBox(
            left_panel,
            width=350,
            height=40,
            font=ctk.CTkFont(size=14),
            values=[name for _, name in categories],
            variable=self.category_var,
            state="readonly",
            corner_radius=10
        )
        category_combo.pack(pady=5)
        if categories:
            category_combo.set(categories[0][1])
        
        # Price
        ctk.CTkLabel(left_panel, text="Price ($)", font=ctk.CTkFont(size=14),
                    text_color="#B0B0B0").pack(pady=(10, 5))
        self.item_price = ctk.CTkEntry(left_panel, width=350, height=40,
                                      font=ctk.CTkFont(size=14), corner_radius=10)
        self.item_price.pack(pady=5)
        
        # Availability
        self.availability_var = ctk.BooleanVar(value=True)
        availability_check = ctk.CTkCheckBox(
            left_panel,
            text="Available",
            variable=self.availability_var,
            font=ctk.CTkFont(size=14),
            corner_radius=5
        )
        availability_check.pack(pady=15)
        
        # Buttons
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=20)
        
        ctk.CTkButton(
            btn_frame, text="➕ Add Item", font=ctk.CTkFont(size=14, weight="bold"),
            width=160, height=45, corner_radius=10, fg_color="#43A047", hover_color="#2E7D32",
            command=self.add_food_item
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="✏️ Update", font=ctk.CTkFont(size=14, weight="bold"),
            width=160, height=45, corner_radius=10, fg_color="#FF9800", hover_color="#F57C00",
            command=self.update_food_item
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Delete", font=ctk.CTkFont(size=14, weight="bold"),
            width=160, height=45, corner_radius=10, fg_color="#F44336", hover_color="#D32F2F",
            command=self.delete_food_item
        ).pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(
            btn_frame, text="🔄 Clear", font=ctk.CTkFont(size=14, weight="bold"),
            width=160, height=45, corner_radius=10, fg_color="#607D8B", hover_color="#455A64",
            command=self.clear_form
        ).pack(side="right", padx=5, pady=10)
        
        # Right panel - Food items list
        right_panel = ctk.CTkFrame(main_container, corner_radius=15, fg_color="#1E1E1E")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            right_panel,
            text="Food Items List",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=15)
        
        # Treeview with custom style
        tree_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                       fieldbackground="#2b2b2b", borderwidth=0, rowheight=35)
        style.configure("Treeview.Heading", background="#1E88E5", foreground="white",
                       borderwidth=0, font=('Arial', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#1E88E5')])
        
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.food_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Category", "Price", "Available"),
            show='headings',
            yscrollcommand=scrollbar.set,
            style="Treeview"
        )
        
        self.food_tree.heading("ID", text="ID")
        self.food_tree.heading("Name", text="Item Name")
        self.food_tree.heading("Category", text="Category")
        self.food_tree.heading("Price", text="Price")
        self.food_tree.heading("Available", text="Status")
        
        self.food_tree.column("ID", width=60)
        self.food_tree.column("Name", width=250)
        self.food_tree.column("Category", width=150)
        self.food_tree.column("Price", width=100)
        self.food_tree.column("Available", width=100)
        
        self.food_tree.pack(fill="both", expand=True)
        scrollbar.configure(command=self.food_tree.yview)
        
        self.food_tree.bind('<ButtonRelease-1>', self.on_food_select)
        
        self.load_food_items()
    
    def load_food_items(self):
        """Load food items into treeview"""
        for item in self.food_tree.get_children():
            self.food_tree.delete(item)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.item_id, f.item_name, c.category_name, f.price, f.availability
                FROM food_items f
                JOIN categories c ON f.category_id = c.category_id
                ORDER BY f.item_id
            """)
            
            for row in cursor.fetchall():
                available = "✅ Yes" if row[4] else "❌ No"
                self.food_tree.insert('', 'end', values=(row[0], row[1], row[2], f"${row[3]:.2f}", available))
            
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load food items: {e}")
    
    def on_food_select(self, event):
        """Handle food item selection"""
        selection = self.food_tree.selection()
        if selection:
            item = self.food_tree.item(selection[0])
            values = item['values']
            
            self.selected_item_id = values[0]
            self.item_name.delete(0, 'end')
            self.item_name.insert(0, values[1])
            self.category_var.set(values[2])
            self.item_price.delete(0, 'end')
            self.item_price.insert(0, str(values[3]).replace('$', ''))
            self.availability_var.set("✅" in values[4])
    
    def add_food_item(self):
        """Add new food item"""
        name = self.item_name.get().strip()
        category = self.category_var.get()
        price = self.item_price.get().strip()
        available = self.availability_var.get()
        
        if not name or not category or not price:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            price = float(price)
            if price < 0:
                messagebox.showerror("Error", "Price cannot be negative")
                return
            
            category_id = self.category_dict[category]
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO food_items (item_name, category_id, price, availability) VALUES (%s, %s, %s, %s)",
                (name, category_id, price, available)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Food item added successfully!")
            self.clear_form()
            self.load_food_items()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")
    
    def update_food_item(self):
        """Update selected food item"""
        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Warning", "Please select an item to update")
            return
        
        name = self.item_name.get().strip()
        category = self.category_var.get()
        price = self.item_price.get().strip()
        available = self.availability_var.get()
        
        if not name or not category or not price:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            price = float(price)
            if price < 0:
                messagebox.showerror("Error", "Price cannot be negative")
                return
            
            category_id = self.category_dict[category]
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE food_items SET item_name=%s, category_id=%s, price=%s, availability=%s WHERE item_id=%s",
                (name, category_id, price, available, self.selected_item_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Food item updated successfully!")
            self.clear_form()
            self.load_food_items()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")
    
    def delete_food_item(self):
        """Delete selected food item"""
        if not hasattr(self, 'selected_item_id'):
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM food_items WHERE item_id=%s", (self.selected_item_id,))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Food item deleted successfully!")
                self.clear_form()
                self.load_food_items()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete item: {e}")
    
    def clear_form(self):
        """Clear form fields"""
        self.item_name.delete(0, 'end')
        self.item_price.delete(0, 'end')
        self.availability_var.set(True)
        if hasattr(self, 'selected_item_id'):
            delattr(self, 'selected_item_id')
    
    def view_menu(self):
        """View all menu items"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📖 Restaurant Menu",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="← Back",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#424242",
            hover_color="#616161",
            command=self.show_dashboard
        ).pack(side="right", padx=30)
        
        # Content
        content = ctk.CTkFrame(self.window, corner_radius=15, fg_color="#1E1E1E")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Treeview
        tree_frame = ctk.CTkFrame(content, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        style = ttk.Style()
        style.configure("Menu.Treeview", rowheight=40, font=('Arial', 12))
        
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Item", "Category", "Price", "Status"),
            show='headings',
            yscrollcommand=scrollbar.set,
            style="Menu.Treeview"
        )
        
        tree.heading("Item", text="Item Name")
        tree.heading("Category", text="Category")
        tree.heading("Price", text="Price")
        tree.heading("Status", text="Availability")
        
        tree.column("Item", width=350)
        tree.column("Category", width=250)
        tree.column("Price", width=150)
        tree.column("Status", width=150)
        
        tree.pack(fill="both", expand=True)
        scrollbar.configure(command=tree.yview)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.item_name, c.category_name, f.price, f.availability
                FROM food_items f
                JOIN categories c ON f.category_id = c.category_id
                ORDER BY c.category_name, f.item_name
            """)
            
            for row in cursor.fetchall():
                status = "✅ Available" if row[3] else "❌ Not Available"
                tree.insert('', 'end', values=(row[0], row[1], f"${row[2]:.2f}", status))
            
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load menu: {e}")
    
    def view_orders(self):
        """View all orders"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📋 Order History",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="← Back",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#424242",
            hover_color="#616161",
            command=self.show_dashboard
        ).pack(side="right", padx=30)
        
        # Content
        content = ctk.CTkFrame(self.window, corner_radius=15, fg_color="#1E1E1E")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Treeview
        tree_frame = ctk.CTkFrame(content, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Order ID", "Staff", "Date", "Total", "Payment", "Status"),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        tree.heading("Order ID", text="Order ID")
        tree.heading("Staff", text="Staff")
        tree.heading("Date", text="Date & Time")
        tree.heading("Total", text="Total")
        tree.heading("Payment", text="Payment")
        tree.heading("Status", text="Status")
        
        tree.column("Order ID", width=100)
        tree.column("Staff", width=150)
        tree.column("Date", width=200)
        tree.column("Total", width=120)
        tree.column("Payment", width=120)
        tree.column("Status", width=120)
        
        tree.pack(fill="both", expand=True)
        scrollbar.configure(command=tree.yview)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_id, u.username, o.order_date, o.total_amount, 
                       o.payment_method, o.payment_status
                FROM orders o
                JOIN users u ON o.staff_id = u.user_id
                ORDER BY o.order_date DESC
            """)
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=(
                    row[0], row[1], row[2].strftime("%Y-%m-%d %H:%M"),
                    f"${row[3]:.2f}", row[4].capitalize(), row[5].capitalize()
                ))
            
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {e}")
    
    def sales_reports(self):
        """Generate sales reports"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📊 Sales Reports",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="← Back",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#424242",
            hover_color="#616161",
            command=self.show_dashboard
        ).pack(side="right", padx=30)
        
        # Content
        content = ctk.CTkFrame(self.window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Statistics
            cursor.execute("SELECT SUM(total_amount) FROM orders WHERE payment_status='completed'")
            total_sales = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(*) FROM orders")
            total_orders = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT SUM(total_amount) FROM orders 
                WHERE DATE(order_date) = CURDATE() AND payment_status='completed'
            """)
            today_sales = cursor.fetchone()[0] or 0
            
            # Summary cards
            summary_frame = ctk.CTkFrame(content, fg_color="transparent")
            summary_frame.pack(fill="x", pady=20)
            
            cards = [
                ("💰 Total Sales", f"${total_sales:.2f}", '#43A047'),
                ("📦 Total Orders", str(total_orders), '#1E88E5'),
                ("🕐 Today's Sales", f"${today_sales:.2f}", '#FF7043')
            ]
            
            for title, value, color in cards:
                card = ctk.CTkFrame(summary_frame, corner_radius=15, fg_color=color, height=120)
                card.pack(side="left", padx=15, fill="both", expand=True)
                
                ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18), 
                           text_color="white").pack(pady=(25, 10))
                ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"),
                           text_color="white").pack()
            
            # Top items
            ctk.CTkLabel(
                content,
                text="🏆 Top 5 Selling Items",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="#FFD700"
            ).pack(pady=20)
            
            cursor.execute("""
                SELECT f.item_name, SUM(oi.quantity) as total_qty
                FROM order_items oi
                JOIN food_items f ON oi.item_id = f.item_id
                GROUP BY f.item_name
                ORDER BY total_qty DESC
                LIMIT 5
            """)
            top_items = cursor.fetchall()
            
            tree_frame = ctk.CTkFrame(content, corner_radius=15, fg_color="#1E1E1E")
            tree_frame.pack(fill="both", expand=True, pady=10)
            
            tree = ttk.Treeview(tree_frame, columns=("Item", "Quantity"), show='headings', height=10)
            tree.heading("Item", text="Item Name")
            tree.heading("Quantity", text="Total Sold")
            tree.column("Item", width=500)
            tree.column("Quantity", width=200)
            tree.pack(fill="both", expand=True, padx=20, pady=20)
            
            for item, qty in top_items:
                tree.insert('', 'end', values=(item, qty))
            
            cursor.close()
            conn.close()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def manage_users(self):
        """Manage system users"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="👥 Manage Users",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="← Back",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#424242",
            hover_color="#616161",
            command=self.show_dashboard
        ).pack(side="right", padx=30)
        
        # Content
        content = ctk.CTkFrame(self.window, corner_radius=15, fg_color="#1E1E1E")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Treeview
        tree_frame = ctk.CTkFrame(content, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree