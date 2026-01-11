import customtkinter as ctk
from tkinter import messagebox, ttk
from db_connection import get_connection
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StaffDashboard:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.cart = []
        
        self.window = ctk.CTk()
        self.window.title("Staff Dashboard")
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
            text="👨‍🍳 Staff Dashboard",
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
        content.pack(fill="both", expand=True, padx=60, pady=50)
        
        # Button grid with icons and colors
        buttons = [
            ("🛒 Take Order", self.take_order, '#43A047'),
            ("📖 View Menu", self.view_menu, '#1E88E5'),
            ("📋 Order History", self.order_history, '#AB47BC'),
            ("🚪 Logout", self.logout, '#EF5350')
        ]
        
        row, col = 0, 0
        for text, command, color in buttons:
            btn = ctk.CTkButton(
                content,
                text=text,
                font=ctk.CTkFont(size=24, weight="bold"),
                width=500,
                height=200,
                corner_radius=20,
                fg_color=color,
                hover_color=self.darken_color(color),
                command=command
            )
            btn.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Configure grid
        for i in range(2):
            content.columnconfigure(i, weight=1)
            content.rowconfigure(i, weight=1)
    
    def darken_color(self, color):
        """Darken a hex color"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def take_order(self):
        """Take customer order"""
        self.clear_window()
        self.cart = []
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🛒 Take Order",
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
        
        # Left panel - Menu items
        left_panel = ctk.CTkFrame(main_container, corner_radius=15, fg_color="#1E1E1E")
        left_panel.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            left_panel,
            text="🍽️ Available Items",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=15)
        
        # Search
        search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=ctk.CTkFont(size=18)
        ).pack(side="left", padx=5)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search menu items...",
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=10
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Menu treeview
        menu_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Menu.Treeview", background="#2b2b2b", foreground="white",
                       fieldbackground="#2b2b2b", borderwidth=0, rowheight=35)
        style.configure("Menu.Treeview.Heading", background="#43A047", foreground="white",
                       borderwidth=0, font=('Arial', 11, 'bold'))
        style.map('Menu.Treeview', background=[('selected', '#43A047')])
        
        menu_scroll = ctk.CTkScrollbar(menu_frame)
        menu_scroll.pack(side="right", fill="y")
        
        self.menu_tree = ttk.Treeview(
            menu_frame,
            columns=("ID", "Item", "Category", "Price"),
            show='headings',
            yscrollcommand=menu_scroll.set,
            style="Menu.Treeview"
        )
        
        self.menu_tree.heading("ID", text="ID")
        self.menu_tree.heading("Item", text="Item Name")
        self.menu_tree.heading("Category", text="Category")
        self.menu_tree.heading("Price", text="Price")
        
        self.menu_tree.column("ID", width=50)
        self.menu_tree.column("Item", width=200)
        self.menu_tree.column("Category", width=130)
        self.menu_tree.column("Price", width=80)
        
        self.menu_tree.pack(fill="both", expand=True)
        menu_scroll.configure(command=self.menu_tree.yview)
        
        # Add to cart controls
        add_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        add_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            add_frame,
            text="Quantity:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        self.qty_var = ctk.StringVar(value="1")
        qty_spinbox = ctk.CTkEntry(
            add_frame,
            width=80,
            height=40,
            font=ctk.CTkFont(size=14),
            textvariable=self.qty_var,
            justify="center"
        )
        qty_spinbox.pack(side="left", padx=5)
        
        ctk.CTkButton(
            add_frame,
            text="➕ Add to Cart",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=10,
            fg_color="#43A047",
            hover_color="#2E7D32",
            command=self.add_to_cart
        ).pack(side="right", padx=10, fill="x", expand=True)
        
        # Right panel - Cart
        right_panel = ctk.CTkFrame(main_container, width=450, corner_radius=15, fg_color="#1E1E1E")
        right_panel.pack(side="right", fill="both", padx=10)
        right_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            right_panel,
            text="🛒 Order Cart",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=15)
        
        # Cart treeview
        cart_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        cart_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        style.configure("Cart.Treeview", rowheight=40)
        style.configure("Cart.Treeview.Heading", background="#1E88E5")
        style.map('Cart.Treeview', background=[('selected', '#1E88E5')])
        
        cart_scroll = ctk.CTkScrollbar(cart_frame)
        cart_scroll.pack(side="right", fill="y")
        
        self.cart_tree = ttk.Treeview(
            cart_frame,
            columns=("Item", "Qty", "Price", "Total"),
            show='headings',
            yscrollcommand=cart_scroll.set,
            style="Cart.Treeview"
        )
        
        self.cart_tree.heading("Item", text="Item")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Total", text="Total")
        
        self.cart_tree.column("Item", width=180)
        self.cart_tree.column("Qty", width=50)
        self.cart_tree.column("Price", width=70)
        self.cart_tree.column("Total", width=70)
        
        self.cart_tree.pack(fill="both", expand=True)
        cart_scroll.configure(command=self.cart_tree.yview)
        
        # Total frame
        total_frame = ctk.CTkFrame(right_panel, corner_radius=10, fg_color="#2E7D32", height=60)
        total_frame.pack(fill="x", padx=15, pady=10)
        total_frame.pack_propagate(False)
        
        self.total_label = ctk.CTkLabel(
            total_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.total_label.pack(pady=15)
        
        # Cart buttons
        cart_btn_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        cart_btn_frame.pack(pady=10, padx=15, fill="x")
        
        ctk.CTkButton(
            cart_btn_frame,
            text="🗑️ Remove Item",
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10,
            fg_color="#EF5350",
            hover_color="#D32F2F",
            command=self.remove_from_cart
        ).pack(pady=5, fill="x")
        
        ctk.CTkButton(
            cart_btn_frame,
            text="🔄 Clear Cart",
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10,
            fg_color="#757575",
            hover_color="#616161",
            command=self.clear_cart
        ).pack(pady=5, fill="x")
        
        ctk.CTkButton(
            cart_btn_frame,
            text="✅ Place Order",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            corner_radius=10,
            fg_color="#43A047",
            hover_color="#2E7D32",
            command=self.place_order
        ).pack(pady=10, fill="x")
        
        # Load menu items
        self.load_menu_items()
        
        # Search functionality
        def search_items(*args):
            search_text = search_entry.get().lower()
            for item in self.menu_tree.get_children():
                self.menu_tree.delete(item)
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT f.item_id, f.item_name, c.category_name, f.price
                    FROM food_items f
                    JOIN categories c ON f.category_id = c.category_id
                    WHERE f.availability = TRUE AND 
                          (LOWER(f.item_name) LIKE %s OR LOWER(c.category_name) LIKE %s)
                    ORDER BY c.category_name, f.item_name
                """, (f'%{search_text}%', f'%{search_text}%'))
                
                for row in cursor.fetchall():
                    self.menu_tree.insert('', 'end', values=(row[0], row[1], row[2], f"${row[3]:.2f}"))
                
                cursor.close()
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {e}")
        
        search_entry.bind('<KeyRelease>', search_items)
    
    def load_menu_items(self):
        """Load available menu items"""
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.item_id, f.item_name, c.category_name, f.price
                FROM food_items f
                JOIN categories c ON f.category_id = c.category_id
                WHERE f.availability = TRUE
                ORDER BY c.category_name, f.item_name
            """)
            
            for row in cursor.fetchall():
                self.menu_tree.insert('', 'end', values=(row[0], row[1], row[2], f"${row[3]:.2f}"))
            
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load menu: {e}")
    
    def add_to_cart(self):
        """Add selected item to cart"""
        selection = self.menu_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        try:
            quantity = int(self.qty_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return
        
        item = self.menu_tree.item(selection[0])
        values = item['values']
        
        item_id = values[0]
        item_name = values[1]
        price = float(values[3].replace('$', ''))
        
        # Check if item already in cart
        for i, cart_item in enumerate(self.cart):
            if cart_item['id'] == item_id:
                self.cart[i]['quantity'] += quantity
                self.update_cart_display()
                self.qty_var.set("1")
                return
        
        # Add new item to cart
        self.cart.append({
            'id': item_id,
            'name': item_name,
            'price': price,
            'quantity': quantity
        })
        
        self.update_cart_display()
        self.qty_var.set("1")
    
    def update_cart_display(self):
        """Update cart treeview"""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        total = 0
        for item in self.cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            self.cart_tree.insert('', 'end', values=(
                item['name'], item['quantity'],
                f"${item['price']:.2f}", f"${subtotal:.2f}"
            ))
        
        self.total_label.configure(text=f"Total: ${total:.2f}")
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        item = self.cart_tree.item(selection[0])
        item_name = item['values'][0]
        
        self.cart = [item for item in self.cart if item['name'] != item_name]
        self.update_cart_display()
    
    def clear_cart(self):
        """Clear all items from cart"""
        if self.cart and messagebox.askyesno("Confirm", "Clear all items from cart?"):
            self.cart = []
            self.update_cart_display()
    
    def place_order(self):
        """Place the order"""
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        # Payment method selection
        payment_window = ctk.CTkToplevel(self.window)
        payment_window.title("Payment")
        payment_window.geometry("450x400")
        
        # Center window
        payment_window.update_idletasks()
        x = (payment_window.winfo_screenwidth() // 2) - 225
        y = (payment_window.winfo_screenheight() // 2) - 200
        payment_window.geometry(f'450x400+{x}+{y}')
        
        payment_window.transient(self.window)
        payment_window.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(payment_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            main_frame,
            text="💳 Select Payment Method",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=30)
        
        payment_var = ctk.StringVar(value="cash")
        
        # Payment options
        payment_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        payment_frame.pack(pady=20)
        
        ctk.CTkRadioButton(
            payment_frame,
            text="💵 Cash",
            variable=payment_var,
            value="cash",
            font=ctk.CTkFont(size=16),
            radiobutton_width=20,
            radiobutton_height=20
        ).pack(pady=10, anchor="w")
        
        ctk.CTkRadioButton(
            payment_frame,
            text="💳 Card",
            variable=payment_var,
            value="card",
            font=ctk.CTkFont(size=16),
            radiobutton_width=20,
            radiobutton_height=20
        ).pack(pady=10, anchor="w")
        
        ctk.CTkRadioButton(
            payment_frame,
            text="🌐 Online",
            variable=payment_var,
            value="online",
            font=ctk.CTkFont(size=16),
            radiobutton_width=20,
            radiobutton_height=20
        ).pack(pady=10, anchor="w")
        
        def confirm_payment():
            payment_method = payment_var.get()
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Calculate total
                total = sum(item['price'] * item['quantity'] for item in self.cart)
                
                # Insert order
                cursor.execute("""
                    INSERT INTO orders (staff_id, total_amount, payment_method, payment_status)
                    VALUES (%s, %s, %s, 'completed')
                """, (self.user_id, total, payment_method))
                
                order_id = cursor.lastrowid
                
                # Insert order items
                for item in self.cart:
                    subtotal = item['price'] * item['quantity']
                    cursor.execute("""
                        INSERT INTO order_items (order_id, item_id, quantity, item_price, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (order_id, item['id'], item['quantity'], item['price'], subtotal))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                payment_window.destroy()
                messagebox.showinfo(
                    "Success",
                    f"✅ Order placed successfully!\n\n"
                    f"Order ID: {order_id}\n"
                    f"Total: ${total:.2f}\n"
                    f"Payment: {payment_method.capitalize()}"
                )
                
                self.cart = []
                self.update_cart_display()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to place order: {e}")
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="✅ Confirm Payment",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            corner_radius=10,
            fg_color="#43A047",
            hover_color="#2E7D32",
            command=confirm_payment
        ).pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancel",
            font=ctk.CTkFont(size=14),
            width=300,
            height=45,
            corner_radius=10,
            fg_color="#EF5350",
            hover_color="#D32F2F",
            command=payment_window.destroy
        ).pack()
    
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
        style.configure("ViewMenu.Treeview", rowheight=40, font=('Arial', 12))
        style.configure("ViewMenu.Treeview.Heading", background="#1E88E5")
        
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Item", "Category", "Price", "Status"),
            show='headings',
            yscrollcommand=scrollbar.set,
            style="ViewMenu.Treeview"
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
    
    def order_history(self):
        """View order history for this staff"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📋 My Order History",
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
            columns=("Order ID", "Date", "Total", "Payment", "Status"),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        tree.heading("Order ID", text="Order ID")
        tree.heading("Date", text="Date & Time")
        tree.heading("Total", text="Total Amount")
        tree.heading("Payment", text="Payment Method")
        tree.heading("Status", text="Status")
        
        tree.column("Order ID", width=100)
        tree.column("Date", width=250)
        tree.column("Total", width=150)
        tree.column("Payment", width=150)
        tree.column("Status", width=150)
        
        tree.pack(fill="both", expand=True)
        scrollbar.configure(command=tree.yview)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT order_id, order_date, total_amount, payment_method, payment_status
                FROM orders
                WHERE staff_id = %s
                ORDER BY order_date DESC
            """, (self.user_id,))
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=(
                    row[0], row[1].strftime("%Y-%m-%d %H:%M"),
                    f"${row[2]:.2f}", row[3].capitalize(), row[4].capitalize()
                ))
            
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load order history: {e}")
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.window.destroy()
            from login import LoginWindow
            LoginWindow().run()
    
    def clear_window(self):
        """Clear all widgets"""
        for widget in self.window.winfo_children():
            widget.destroy()