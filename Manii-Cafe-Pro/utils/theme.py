import customtkinter as ctk

COLORS = {
    "background": "#0F1115",
    "sidebar": "#151820",
    "card": "#1B1F27",
    "card_light": "#222731",
    "gold": "#D4A853",
    "gold_hover": "#E2BC6B",
    "text": "#F5F5F5",
    "text_secondary": "#9CA3AF",
    "muted": "#6B7280",
    "border": "#2A2F3A",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "white": "#FFFFFF",
    "black": "#000000",
}

FONTS = {
    "title": ("Segoe UI", 28, "bold"),
    "heading": ("Segoe UI", 20, "bold"),
    "subheading": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 14),
    "small": ("Segoe UI", 12),
    "stat": ("Segoe UI", 26, "bold"),
}

def setup_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
