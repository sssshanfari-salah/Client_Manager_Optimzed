"""Client record actions for the main client manager window."""

from tkinter import messagebox

from app.domain.clients_management import Client
from app.i18n.translations import CURRENT_LANGUAGE, T, set_language


class ClientActions:
    """Actions for creating and saving client records."""

    def switch_language(self, event=None):
        selected = self.language_var.get()
        set_language(selected)
        self.language_var.set(CURRENT_LANGUAGE)
        self.refresh_lang_ui()

    def save_current_client(self):
        name = self.client_name_var.get().strip()
        if not name or name == "<New Client>":
            messagebox.showwarning(T("Missing client"), T("Please enter a client name before saving."))
            return

        self.client_manager.load_clients()
        existing = next((client for client in self.client_manager.clients if client.name.lower() == name.lower()), None)
        if existing is None:
            existing = Client(name, self.contact_var.get().strip(), self.business_var.get().strip(), self.email_var.get().strip())
            self.client_manager.clients.append(existing)
        else:
            existing.contact = self.contact_var.get().strip()
            existing.business = self.business_var.get().strip()
            existing.email = self.email_var.get().strip()

        self.client_manager.save_clients()
        messagebox.showinfo(T("Client saved"), T("Client saved successfully."))
