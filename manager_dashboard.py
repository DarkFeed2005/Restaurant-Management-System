import customtkinter as ctk
from tkinter import messagebox
from db_connection import get_connection
from datetime import datetime

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
        
        # Button grid
        buttons = [
            ("🍔 Manage Menu", self.manage_menu, '#1E88E5'),
            ("📊 View Reports", self.view_reports, '#FF9800'),
            ("👥 Manage Users", self.manage_users, '#AB47BC'),
            ("📋 All Orders", self.view_all_orders, '#26A69A'),
            ("📈 Statistics", self.view_statistics, '#EF5350'),
            ("🚪 Logout", self.logout, '#757575')
        ]
        
        row, col = 0, 0
        for text, command, color in buttons:
            btn = ctk.CTkButton(
                content,
                text=text,
                font=ctk.CTkFont(size=22, weight="bold"),
                width=400,
                height=160,
                corner_radius=20,
                fg_color=color,
                hover_color=self.darken_color(color),
                command=command
            )
            btn.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
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
        """Manage menu items"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🍔 Manage Menu",
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
        
        ctk.CTkButton(
            header,
            text="➕ Add New Item",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=150,
            height=40,
            corner_radius=10,
            fg_color="#43A047",
            hover_color="#2E7D32",
            command=self.add_menu_item
        ).pack(side="right", padx=10)
        
        # Content
        content = ctk.CTkFrame(self.window, corner_radius=15, fg_color="#1E1E1E")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(content, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.load_menu_items_manager(scroll_frame)
    
    def load_menu_items_manager(self, parent):
        """Load menu items for manager"""
        try:
            conn = get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.item_id, f.item_name, c.category_name, f.price, f.availability
                FROM food_items f
                JOIN categories c ON f.category_id = c.category_id
                ORDER BY c.category_name, f.item_name
            """)
            
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            
            for item_id, item_name, category, price, availability in items:
                item_card = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=10)
                item_card.pack(fill="x", padx=10, pady=8)
                
                info_frame = ctk.CTkFrame(item_card, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=item_name,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    anchor="w"
                ).pack(anchor="w")
                
                status = "✅ Available" if availability else "❌ Unavailable"
                status_color = "#43A047" if availability else "#EF5350"
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Category: {category}  •  Price: ${price:.2f}  •  {status}",
                    font=ctk.CTkFont(size=14),
                    text_color="#888888",
                    anchor="w"
                ).pack(anchor="w")
                
                btn_frame = ctk.CTkFrame(item_card, fg_color="transparent")
                btn_frame.pack(side="right", padx=15, pady=10)
                
                ctk.CTkButton(
                    btn_frame,
                    text="✏️ Edit",
                    width=80,
                    height=35,
                    corner_radius=8,
                    fg_color="#1E88E5",
                    hover_color="#1565C0",
                    command=lambda i=item_id: self.edit_menu_item(i)
                ).pack(side="left", padx=5)
                
                ctk.CTkButton(
                    btn_frame,
                    text="🗑️ Delete",
                    width=80,
                    height=35,
                    corner_radius=8,
                    fg_color="#EF5350",
                    hover_color="#D32F2F",
                    command=lambda i=item_id, n=item_name: self.delete_menu_item(i, n)
                ).pack(side="left", padx=5)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load menu: {e}")
    
    def add_menu_item(self):
        """Add new menu item"""
        add_window = ctk.CTkToplevel(self.window)
        add_window.title("Add Menu Item")
        add_window.geometry("500x600")
        add_window.transient(self.window)
        add_window.grab_set()
        
        # Center window
        add_window.update_idletasks()
        x = (add_window.winfo_screenwidth() // 2) - 250
        y = (add_window.winfo_screenheight() // 2) - 300
        add_window.geometry(f'500x600+{x}+{y}')
        
        main_frame = ctk.CTkFrame(add_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            main_frame,
            text="➕ Add New Menu Item",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=(10, 30))
        
        # Item Name
        ctk.CTkLabel(main_frame, text="Item Name", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        name_entry = ctk.CTkEntry(main_frame, width=440, height=45, placeholder_text="Enter item name")
        name_entry.pack(pady=(0, 15))
        
        # Category
        ctk.CTkLabel(main_frame, text="Category", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(5, 5))
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, category_name FROM categories")
            categories = cursor.fetchall()
            cursor.close()
            conn.close()
            
            category_var = ctk.StringVar(value=categories[0][1] if categories else "")
            category_menu = ctk.CTkOptionMenu(
                main_frame,
                values=[cat[1] for cat in categories],
                variable=category_var,
                width=440,
                height=45
            )
            category_menu.pack(pady=(0, 15))
        except:
            category_var = ctk.StringVar(value="Main Course")
            category_menu = ctk.CTkOptionMenu(main_frame, values=["Main Course"], variable=category_var, width=440, height=45)
            category_menu.pack(pady=(0, 15))
        
        # Price
        ctk.CTkLabel(main_frame, text="Price ($)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(5, 5))
        price_entry = ctk.CTkEntry(main_frame, width=440, height=45, placeholder_text="Enter price")
        price_entry.pack(pady=(0, 15))
        
        # Availability
        availability_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            main_frame,
            text="Available",
            variable=availability_var,
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        
        def save_item():
            name = name_entry.get().strip()
            category = category_var.get()
            price = price_entry.get().strip()
            available = availability_var.get()
            
            if not name or not price:
                messagebox.showwarning("Warning", "Please fill all fields!")
                return
            
            try:
                price_val = float(price)
                if price_val <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
                
                conn = get_connection()
                cursor = conn.cursor()
                
                # Get category ID
                cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (category,))
                cat_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    INSERT INTO food_items (item_name, category_id, price, availability)
                    VALUES (%s, %s, %s, %s)
                """, (name, cat_id, price_val, available))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Menu item added successfully!")
                add_window.destroy()
                self.manage_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add item: {e}")
        
        ctk.CTkButton(
            main_frame,
            text="✓ Save Item",
            width=440,
            height=50,
            corner_radius=10,
            fg_color="#43A047",
            hover_color="#2E7D32",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=save_item
        ).pack(pady=20)
    
    def edit_menu_item(self, item_id):
        """Edit menu item"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.item_name, c.category_name, f.price, f.availability
                FROM food_items f
                JOIN categories c ON f.category_id = c.category_id
                WHERE f.item_id = %s
            """, (item_id,))
            
            item_data = cursor.fetchone()
            if not item_data:
                messagebox.showerror("Error", "Item not found!")
                return
            
            item_name, category_name, price, availability = item_data
            
            # Get all categories
            cursor.execute("SELECT category_id, category_name FROM categories")
            categories = cursor.fetchall()
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load item: {e}")
            return
        
        edit_window = ctk.CTkToplevel(self.window)
        edit_window.title("Edit Menu Item")
        edit_window.geometry("500x600")
        edit_window.transient(self.window)
        edit_window.grab_set()
        
        # Center window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - 250
        y = (edit_window.winfo_screenheight() // 2) - 300
        edit_window.geometry(f'500x600+{x}+{y}')
        
        main_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            main_frame,
            text="✏️ Edit Menu Item",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=(10, 30))
        
        # Item Name
        ctk.CTkLabel(main_frame, text="Item Name", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        name_entry = ctk.CTkEntry(main_frame, width=440, height=45)
        name_entry.insert(0, item_name)
        name_entry.pack(pady=(0, 15))
        
        # Category
        ctk.CTkLabel(main_frame, text="Category", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(5, 5))
        category_var = ctk.StringVar(value=category_name)
        category_menu = ctk.CTkOptionMenu(
            main_frame,
            values=[cat[1] for cat in categories],
            variable=category_var,
            width=440,
            height=45
        )
        category_menu.pack(pady=(0, 15))
        
        # Price
        ctk.CTkLabel(main_frame, text="Price ($)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(5, 5))
        price_entry = ctk.CTkEntry(main_frame, width=440, height=45)
        price_entry.insert(0, str(price))
        price_entry.pack(pady=(0, 15))
        
        # Availability
        availability_var = ctk.BooleanVar(value=availability)
        ctk.CTkCheckBox(
            main_frame,
            text="Available",
            variable=availability_var,
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        
        def update_item():
            name = name_entry.get().strip()
            category = category_var.get()
            price = price_entry.get().strip()
            available = availability_var.get()
            
            if not name or not price:
                messagebox.showwarning("Warning", "Please fill all fields!")
                return
            
            try:
                price_val = float(price)
                if price_val <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
                
                conn = get_connection()
                cursor = conn.cursor()
                
                # Get category ID
                cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (category,))
                cat_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    UPDATE food_items
                    SET item_name = %s, category_id = %s, price = %s, availability = %s
                    WHERE item_id = %s
                """, (name, cat_id, price_val, available, item_id))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Menu item updated successfully!")
                edit_window.destroy()
                self.manage_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update item: {e}")
        
        ctk.CTkButton(
            main_frame,
            text="✓ Update Item",
            width=440,
            height=50,
            corner_radius=10,
            fg_color="#1E88E5",
            hover_color="#1565C0",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=update_item
        ).pack(pady=20)
    
    def delete_menu_item(self, item_id, item_name):
        """Delete menu item"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM food_items WHERE item_id = %s", (item_id,))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Menu item deleted successfully!")
                self.manage_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete item: {e}")
    
    def view_reports(self):
        """View sales reports"""
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
            
            # Total sales
            cursor.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders WHERE payment_status = 'completed'")
            total_orders, total_sales = cursor.fetchone()
            
            # Today's sales
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(total_amount), 0) 
                FROM orders 
                WHERE DATE(order_date) = CURDATE() AND payment_status = 'completed'
            """)
            today_orders, today_sales = cursor.fetchone()
            
            # Top selling items
            cursor.execute("""
                SELECT f.item_name, SUM(oi.quantity) as total_qty, SUM(oi.subtotal) as total_sales
                FROM order_items oi
                JOIN food_items f ON oi.item_id = f.item_id
                GROUP BY f.item_id, f.item_name
                ORDER BY total_qty DESC
                LIMIT 5
            """)
            top_items = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Stats cards
            stats_frame = ctk.CTkFrame(content, fg_color="transparent")
            stats_frame.pack(fill="x", pady=20)
            
            stats = [
                ("Total Orders", str(total_orders), "#1E88E5"),
                ("Total Sales", f"${total_sales:.2f}", "#43A047"),
                ("Today's Orders", str(today_orders), "#FF9800"),
                ("Today's Sales", f"${today_sales:.2f}", "#AB47BC")
            ]
            
            for i, (label, value, color) in enumerate(stats):
                card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=15)
                card.grid(row=0, column=i, padx=15, sticky="nsew")
                
                ctk.CTkLabel(
                    card,
                    text=label,
                    font=ctk.CTkFont(size=16),
                    text_color="white"
                ).pack(pady=(20, 5))
                
                ctk.CTkLabel(
                    card,
                    text=value,
                    font=ctk.CTkFont(size=32, weight="bold"),
                    text_color="white"
                ).pack(pady=(5, 20))
                
                stats_frame.columnconfigure(i, weight=1)
            
            # Top selling items
            top_items_frame = ctk.CTkFrame(content, fg_color="#1E1E1E", corner_radius=15)
            top_items_frame.pack(fill="both", expand=True, pady=20)
            
            ctk.CTkLabel(
                top_items_frame,
                text="🏆 Top 5 Selling Items",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="#FFD700"
            ).pack(pady=20)
            
            scroll_frame = ctk.CTkScrollableFrame(top_items_frame, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            for i, (item_name, qty, sales) in enumerate(top_items, 1):
                item_card = ctk.CTkFrame(scroll_frame, fg_color="#2b2b2b", corner_radius=10)
                item_card.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(
                    item_card,
                    text=f"{i}. {item_name}",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    anchor="w"
                ).pack(side="left", padx=20, pady=15)
                
                ctk.CTkLabel(
                    item_card,
                    text=f"Qty: {qty}  •  Sales: ${sales:.2f}",
                    font=ctk.CTkFont(size=14),
                    text_color="#888888"
                ).pack(side="right", padx=20, pady=15)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reports: {e}")
    
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
        
        scroll_frame = ctk.CTkScrollableFrame(content, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, role, created_at FROM users ORDER BY created_at DESC")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            
            for user_id, username, role, created_at in users:
                user_card = ctk.CTkFrame(scroll_frame, fg_color="#2b2b2b", corner_radius=10)
                user_card.pack(fill="x", padx=10, pady=8)
                
                info_frame = ctk.CTkFrame(user_card, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=username,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    anchor="w"
                ).pack(anchor="w")
                
                role_color = "#1E88E5" if role == "manager" else "#43A047"
                ctk.CTkLabel(
                    info_frame,
                    text=f"Role: {role.capitalize()}  •  Joined: {created_at.strftime('%Y-%m-%d')}",
                    font=ctk.CTkFont(size=14),
                    text_color="#888888",
                    anchor="w"
                ).pack(anchor="w")
                
                if user_id != self.user_id:
                    ctk.CTkButton(
                        user_card,
                        text="🗑️ Delete",
                        width=80,
                        height=35,
                        corner_radius=8,
                        fg_color="#EF5350",
                        hover_color="#D32F2F",
                        command=lambda uid=user_id, uname=username: self.delete_user(uid, uname)
                    ).pack(side="right", padx=15, pady=10)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
    
    def delete_user(self, user_id, username):
        """Delete a user"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "User deleted successfully!")
                self.manage_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")
    
    def view_all_orders(self):
        """View all orders"""
        self.clear_window()
        
        # Header
        header = ctk.CTkFrame(self.window, height=80, corner_radius=0, fg_color="#1E1E1E")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="📋 All Orders",
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
        content = ctk.CTkFrame(self.window, corner_radius=15, fg_color