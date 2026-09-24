"""Window classes for task, contract, and payment management views."""

import tkinter as tk
from tkinter import ttk

from ui_shared import BaseWindow


class TaskDetailsWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, client_name="Client", plan=None, all_tasks=None, pending_tasks=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Task Details", geometry="700x500")
        self.configure_window(self)
        self.client_name = client_name
        self.plan = plan
        self.all_tasks = list(all_tasks or [])
        self.pending_tasks = list(pending_tasks or [])


class ContractDetailsWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Contract Details", geometry="600x430")
        self.configure_window(self)


class ReservationContractWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, client_name="", client_data=None):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Reservation Contract", geometry="980x760")
        self.configure_window(self)
        self.client_name = client_name
        self.client_data = client_data

        try:
            from ui_reservation_contract import ShopReservationForm
        except ImportError:
            return

        form = ShopReservationForm(client_name=client_name, client_data=client_data)
        form.transient(self)
        form.grab_set()
        self._contract_form = form


class ClientPaymentReportWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, client_name=""):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Payment Report", geometry="820x540")
        self.configure_window(self)
        self.client_name = client_name


class ClientTransactionsWindow(tk.Toplevel, BaseWindow):
    def __init__(self, master=None, client_name=""):
        tk.Toplevel.__init__(self, master)
        BaseWindow.__init__(self, title="Transactions", geometry="900x520")
        self.configure_window(self)
        self.client_name = client_name


__all__ = [
    "TaskDetailsWindow",
    "ContractDetailsWindow",
    "ReservationContractWindow",
    "ClientPaymentReportWindow",
    "ClientTransactionsWindow",
]
