import customtkinter as ctk
from tkinter import messagebox
import ctypes

# Fix for high-resolution screen scaling
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Restaurant Management System v1.0")
        
        # Set fixed large window size
        self.win_width = 1200
        self.win_height = 700

        # Center window on screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 1.5) - (self.win_width // 1.5)
        y = (screen_height // 1.5) - (self.win_height // 3)
        self.window.geometry(f"{self.win_width}x{self.win_height}+{x}+{y}")
        self.window.resizable(False, False)

        self.current_role = None
        self.show_role_selection()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def show_role_selection(self):
        self.clear_window()

        # --- Left Side: Decorative Branding ---
        left_frame = ctk.CTkFrame(self.window, width=500, corner_radius=0, fg_color="#1a1a1a")
        left_frame.pack(side="left", fill="both", expand=False)

        brand_label = ctk.CTkLabel(
            left_frame, 
            text="🍽️\nRestaurant\nManagement \nSYSTEM", 
            font=ctk.CTkFont(size=60, weight="bold"),
            text_color="#FFD700"
        )
        brand_label.place(relx=0.5, rely=0.4, anchor="center")

        desc_label = ctk.CTkLabel(
            left_frame, 
            text="Efficiency in every serving.", 
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="#888888"
        )
        desc_label.place(relx=0.5, rely=0.9, anchor="center")

        # --- Right Side: Role Selection ---
        right_frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True)

        title_label = ctk.CTkLabel(
            right_frame, 
            text="Welcome Back", 
            font=ctk.CTkFont(size=40, weight="bold")
        )
        title_label.pack(pady=(120, 10))

        subtitle_label = ctk.CTkLabel(
            right_frame, 
            text="Please select your portal to login", 
            font=ctk.CTkFont(size=18),
            text_color="#aaaaaa"
        )
        subtitle_label.pack(pady=(0, 50))

        # Buttons
        btn_style = {"width": 350, "height": 60, "corner_radius": 10, "font": ctk.CTkFont(size=18, weight="bold")}
        
        ctk.CTkButton(right_frame, text="👨‍💼 Manager Portal", fg_color="#1E88E5", hover_color="#1565C0",
                      command=lambda: self.show_login('manager'), **btn_style).pack(pady=10)
        
        ctk.CTkButton(right_frame, text="👨‍🍳 Staff Portal", fg_color="#43A047", hover_color="#2E7D32",
                      command=lambda: self.show_login('staff'), **btn_style).pack(pady=10)
        
        ctk.CTkButton(right_frame, text="Exit Application", fg_color="transparent", border_width=2, 
                      border_color="#D32F2F", text_color="#D32F2F", hover_color="#331111",
                      command=self.window.destroy, **btn_style).pack(pady=(50, 0))

    def show_login(self, role):
        self.current_role = role
        self.clear_window()

        color = '#1E88E5' if role == 'manager' else '#43A047'
        
        # --- Left Side: Contextual Info ---
        left_frame = ctk.CTkFrame(self.window, width=500, corner_radius=0, fg_color=color)
        left_frame.pack(side="left", fill="both")

        ctk.CTkLabel(left_frame, text="Login to your", font=ctk.CTkFont(size=25), text_color="white").place(relx=0.5, rely=0.42, anchor="center")
        ctk.CTkLabel(left_frame, text=f"{role.upper()} ACCOUNT", font=ctk.CTkFont(size=35, weight="bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # --- Right Side: Login Form ---
        right_frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True)

        # Back button top left
        ctk.CTkButton(right_frame, text="← Back", width=80, fg_color="transparent", 
                      command=self.show_role_selection).place(x=20, y=20)

        form_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_container, text="Credentials", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(0, 30))

        # Username
        self.username_entry = ctk.CTkEntry(form_container, width=400, height=50, placeholder_text="Username", corner_radius=10)
        self.username_entry.pack(pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(form_container, width=400, height=50, placeholder_text="Password", show="●", corner_radius=10)
        self.password_entry.pack(pady=10)

        # Login Button
        ctk.CTkButton(form_container, text="Secure Login", width=400, height=50, corner_radius=10,
                      fg_color=color, command=self.login).pack(pady=(30, 10))
        
        # Register Link
        ctk.CTkButton(form_container, text="Need an account? Register here", fg_color="transparent", 
                      text_color="#aaaaaa", hover_color="#2b2b2b", command=self.show_register).pack()

        self.window.bind('<Return>', lambda e: self.login())

    def login(self):
        # Your existing database logic remains the same here
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Fields cannot be empty")
            return
        
        # Mocking connection for this example - Replace with your actual DB call
        messagebox.showinfo("Login", f"Attempting login for {username} as {self.current_role}")

    def show_register(self):
        # Using Toplevel for registration so it doesn't break the main layout flow
        reg_window = ctk.CTkToplevel(self.window)
        reg_window.title("New Registration")
        reg_window.geometry("500x600")
        reg_window.attributes('-topmost', True)
        
        # Add your registration fields here...
        ctk.CTkLabel(reg_window, text="User Registration", font=("Arial", 20, "bold")).pack(pady=20)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()