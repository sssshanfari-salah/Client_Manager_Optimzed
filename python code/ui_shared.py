"""Shared window base classes and common UI entry points."""

from pathlib import Path
import tkinter as tk
from tkinter import ttk


APP_ICON = Path(__file__).resolve().parent.parent / "starco_icon.ico"


class BaseWindow:
    """Common base for windows that share a predictable lifecycle."""

    def __init__(self, *args, title="Window", geometry="700x400", **kwargs):
        self.title_text = title
        self.geometry_size = geometry

    def configure_window(self, root):
        root.title(self.title_text)
        root.geometry(self.geometry_size)
        return root


class WelcomeWindow(tk.Tk, BaseWindow):
    def __init__(self):
        tk.Tk.__init__(self)
        BaseWindow.__init__(self, title="Welcome", geometry="700x340")
        self.configure_window(self)


class ProgressApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client Progress Manager")
        self.geometry("1100x700")


def build_startup_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#09111d")
    splash.geometry("600x400")
    return splash


def open_overview_window():
    return ProgressApp()


def open_welcome_home():
    WelcomeWindow().mainloop()


def safe_main():
    welcome = WelcomeWindow()
    welcome.mainloop()


__all__ = [
    "APP_ICON",
    "BaseWindow",
    "WelcomeWindow",
    "ProgressApp",
    "build_startup_splash",
    "open_overview_window",
    "open_welcome_home",
    "safe_main",
]
