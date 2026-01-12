"""
Theme configuration for Restaurant Management System
"""

import customtkinter as ctk

class Theme:
    # Color Scheme
    PRIMARY = "#2C3E50"
    SECONDARY = "#3498DB"
    ACCENT = "#E74C3C"
    SUCCESS = "#27AE60"
    WARNING = "#F39C12"
    DARK_BG = "#1A1A2E"
    CARD_BG = "#16213E"
    TEXT_LIGHT = "#FFFFFF"
    TEXT_DARK = "#2C3E50"
    TEXT_GRAY = "#95A5A6"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    TITLE_FONT = (FONT_FAMILY, 28, "bold")
    HEADING_FONT = (FONT_FAMILY, 22, "bold")
    SUBHEADING_FONT = (FONT_FAMILY, 16, "bold")
    BODY_FONT = (FONT_FAMILY, 14)
    SMALL_FONT = (FONT_FAMILY, 12)
    
    # UI Settings
    CORNER_RADIUS = 15
    BUTTON_HEIGHT = 45
    INPUT_HEIGHT = 45
    PADDING = 20
    
    @staticmethod
    def setup():
        """Setup the application theme"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    @staticmethod
    def create_card(parent, **kwargs):
        """Create a card widget with consistent styling"""
        return ctk.CTkFrame(
            parent,
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.CARD_BG,
            border_width=1,
            border_color=Theme.PRIMARY,
            **kwargs
        )
    
    @staticmethod
    def create_button(parent, text, command, **kwargs):
        """Create a button with consistent styling"""
        default_kwargs = {
            'font': (Theme.FONT_FAMILY, 14, "bold"),
            'height': Theme.BUTTON_HEIGHT,
            'corner_radius': Theme.CORNER_RADIUS,
            'fg_color': Theme.SECONDARY,
            'hover_color': "#2980B9",
            'text_color': Theme.TEXT_LIGHT,
        }
        default_kwargs.update(kwargs)
        return ctk.CTkButton(parent, text=text, command=command, **default_kwargs)
    
    @staticmethod
    def create_title(parent, text):
        """Create a title label"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=Theme.TITLE_FONT,
            text_color=Theme.TEXT_LIGHT
        )
    
    @staticmethod
    def create_heading(parent, text):
        """Create a heading label"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=Theme.HEADING_FONT,
            text_color=Theme.TEXT_LIGHT
        )