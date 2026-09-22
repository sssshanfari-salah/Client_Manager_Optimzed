"""Window classes for client detail and overview screens."""

import tkinter as tk
from tkinter import ttk

from ui_shared import BaseWindow


class ClientDetailsWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Client Details", geometry="720x520")
        self.configure_window(self)


class AllClientsProgressWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="All Clients Progress", geometry="980x620")
        self.configure_window(self)


__all__ = ["ClientDetailsWindow", "AllClientsProgressWindow"]
