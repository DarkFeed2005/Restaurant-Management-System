# main.py
"""
Restaurant Management System
Main entry point for the application

Built with CustomTkinter for modern UI
"""

from login import LoginWindow
import theme

if __name__ == "__main__":
    theme.Theme.setup_theme()
    app = LoginWindow()
    app.run()