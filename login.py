import customtkinter as ctk
from tkinter import messagebox
from db_connection import get_connection

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Restaurant Management System")
        self.window.geometry("1200x700")
        
        # Center window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.current_role = None
        self.show_role_selection()
        
    def show_role_selection(self):
        """Display role selection screen"""
        self.clear_window()
        
        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Title
        title_label = ctk.CTkLabel(
            main_container, 
            text="🍽️ Restaurant Management System",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=(0, 20))
        
        subtitle_label = ctk.CTkLabel(
            main_container, 
            text="Select Your Role to Continue",
            font=ctk.CTkFont(size=24),
            text_color="#B0B0B0"
        )
        subtitle_label.pack(pady=(0, 60))
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Manager button
        manager_btn = ctk.CTkButton(
            btn_frame,
            text="👨‍💼 Manager",
            font=ctk.CTkFont(size=22, weight="bold"),
            width=300,
            height=80,
            corner_radius=15,
            fg_color="#1E88E5",
            hover_color="#1565C0",
            command=lambda: self.show_login('manager')
        )
        manager_btn.pack(pady=15)
        
        # Staff button
        staff_btn = ctk.CTkButton(
            btn_frame,
            text="👨‍🍳 Staff",
            font=ctk.CTkFont(size=22, weight="bold"),
            width=300,
            height=80,
            corner_radius=15,
            fg_color="#43A047",
            hover_color="#2E7D32",
            command=lambda: self.show_login('staff')
        )
        staff_btn.pack(pady=15)
        
        # Exit button
        exit_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Exit",
            font=ctk.CTkFont(size=18),
            width=300,
            height=60,
            corner_radius=15,
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=self.window.destroy
        )
        exit_btn.pack(pady=15)
    
    def show_login(self, role):
        """Display login screen for selected role"""
        self.current_role = role
        self.clear_window()
        
        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Login card
        login_card = ctk.CTkFrame(main_container, corner_radius=20, fg_color="#1E1E1E")
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        login_card.configure(width=500, height=600)
        
        # Title
        color = '#1E88E5' if role == 'manager' else '#43A047'
        icon = '👨‍💼' if role == 'manager' else '👨‍🍳'
        
        title_label = ctk.CTkLabel(
            login_card,
            text=f"{icon} {role.capitalize()} Login",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=color
        )
        title_label.pack(pady=(40, 30))
        
        # Username
        username_label = ctk.CTkLabel(
            login_card,
            text="Username",
            font=ctk.CTkFont(size=16),
            text_color="#B0B0B0"
        )
        username_label.pack(pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            login_card,
            width=350,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Enter your username",
            corner_radius=10
        )
        self.username_entry.pack(pady=(0, 15))
        
        # Password
        password_label = ctk.CTkLabel(
            login_card,
            text="Password",
            font=ctk.CTkFont(size=16),
            text_color="#B0B0B0"
        )
        password_label.pack(pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            login_card,
            width=350,
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Enter your password",
            show="●",
            corner_radius=10
        )
        self.password_entry.pack(pady=(0, 25))
        
        # Login button
        login_btn = ctk.CTkButton(
            login_card,
            text="🔐 Login",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=350,
            height=50,
            corner_radius=10,
            fg_color=color,
            hover_color=('#1565C0' if role == 'manager' else '#2E7D32'),
            command=self.login
        )
        login_btn.pack(pady=10)
        
        # Register button
        register_btn = ctk.CTkButton(
            login_card,
            text="📝 Register New User",
            font=ctk.CTkFont(size=16),
            width=350,
            height=45,
            corner_radius=10,
            fg_color="#424242",
            hover_color="#616161",
            command=self.show_register
        )
        register_btn.pack(pady=10)
        
        # Back button
        back_btn = ctk.CTkButton(
            login_card,
            text="← Back",
            font=ctk.CTkFont(size=14),
            width=350,
            height=40,
            corner_radius=10,
            fg_color="transparent",
            border_width=2,
            border_color="#424242",
            hover_color="#424242",
            command=self.show_role_selection
        )
        back_btn.pack(pady=(10, 30))
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
        
        try:
            conn = get_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, role FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()
            
            if result:
                user_id, role = result
                
                if role != self.current_role:
                    messagebox.showerror("Error", f"This user is not a {self.current_role}")
                    cursor.close()
                    conn.close()
                    return
                
                cursor.close()
                conn.close()
                
                # Close login window and open dashboard
                self.window.destroy()
                
                if role == "manager":
                    from manager_dashboard import ManagerDashboard
                    ManagerDashboard(user_id, username)
                else:
                    from staff_dashboard import StaffDashboard
                    StaffDashboard(user_id, username)
            else:
                messagebox.showerror("Error", "Invalid username or password")
                cursor.close()
                conn.close()
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")
    
    def show_register(self):
        """Display registration screen"""
        reg_window = ctk.CTkToplevel(self.window)
        reg_window.title("Register User")
        reg_window.geometry("500x600")
        
        # Center window
        reg_window.update_idletasks()
        x = (reg_window.winfo_screenwidth() // 2) - (250)
        y = (reg_window.winfo_screenheight() // 2) - (300)
        reg_window.geometry(f'500x600+{x}+{y}')
        
        reg_window.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(reg_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="📝 User Registration",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=(0, 30))
        
        # Username
        username_label = ctk.CTkLabel(
            main_frame,
            text="Username",
            font=ctk.CTkFont(size=14),
            text_color="#B0B0B0"
        )
        username_label.pack(pady=(10, 5))
        
        reg_username = ctk.CTkEntry(
            main_frame,
            width=350,
            height=40,
            font=ctk.CTkFont(size=14),
            placeholder_text="Enter username",
            corner_radius=10
        )
        reg_username.pack(pady=(0, 10))
        
        # Password
        password_label = ctk.CTkLabel(
            main_frame,
            text="Password",
            font=ctk.CTkFont(size=14),
            text_color="#B0B0B0"
        )
        password_label.pack(pady=(10, 5))
        
        reg_password = ctk.CTkEntry(
            main_frame,
            width=350,
            height=40,
            font=ctk.CTkFont(size=14),
            placeholder_text="Enter password",
            show="●",
            corner_radius=10
        )
        reg_password.pack(pady=(0, 10))
        
        # Role
        role_label = ctk.CTkLabel(
            main_frame,
            text="Role",
            font=ctk.CTkFont(size=14),
            text_color="#B0B0B0"
        )
        role_label.pack(pady=(10, 5))
        
        role_var = ctk.StringVar(value=self.current_role)
        role_combo = ctk.CTkComboBox(
            main_frame,
            width=350,
            height=40,
            font=ctk.CTkFont(size=14),
            values=["manager", "staff"],
            variable=role_var,
            state="readonly",
            corner_radius=10
        )
        role_combo.pack(pady=(0, 20))
        
        def register():
            username = reg_username.get().strip()
            password = reg_password.get().strip()
            role = role_var.get()
            
            if not username or not password:
                messagebox.showwarning("Warning", "All fields are required")
                return
            
            try:
                conn = get_connection()
                if not conn:
                    return
                    
                cursor = conn.cursor()
                
                # Check if username exists
                cursor.execute("SELECT username FROM users WHERE username=%s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                    cursor.close()
                    conn.close()
                    return
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, role)
                )
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "User registered successfully")
                reg_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {e}")
        
        # Register button
        register_btn = ctk.CTkButton(
            main_frame,
            text="✅ Register",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=350,
            height=50,
            corner_radius=10,
            fg_color="#43A047",
            hover_color="#2E7D32",
            command=register
        )
        register_btn.pack(pady=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="❌ Close",
            font=ctk.CTkFont(size=14),
            width=350,
            height=45,
            corner_radius=10,
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=reg_window.destroy
        )
        close_btn.pack(pady=10)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()