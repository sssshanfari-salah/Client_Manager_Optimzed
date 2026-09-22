"""Window classes for previews and exports."""

import tkinter as tk
from tkinter import ttk

from ui_shared import BaseWindow


class ClientLogPreviewWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, report_text=""):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Preview", geometry="800x520")
        self.configure_window(self)
        self.text = tk.Text(self, wrap="word")
        self.text.pack(fill="both", expand=True)
        self.text.insert("1.0", report_text)
        self.text.configure(state="disabled")


class ExportClientsLogWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, manager=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Export Clients Log", geometry="500x160")
        self.configure_window(self)
        self.manager = manager


class ExportTaskLogWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, plan=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Export Task Log", geometry="500x160")
        self.configure_window(self)
        self.plan = plan


class ExportReviewLogWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Export Review Log", geometry="560x180")
        self.configure_window(self)


class ClientReviewsLogWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, manager=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Client Reviews Log", geometry="1100x560")
        self.configure_window(self)
        self.manager = manager


__all__ = [
    "ClientLogPreviewWindow",
    "ExportClientsLogWindow",
    "ExportTaskLogWindow",
    "ExportReviewLogWindow",
    "ClientReviewsLogWindow",
]
