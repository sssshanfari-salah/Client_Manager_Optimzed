"""State-binding helpers used by the UI controller."""

import tkinter as tk

from app.i18n.translations import CURRENT_LANGUAGE, T, apply_bidi_text


class StateBinding:
    """Mix-in responsible for binding widgets to model state."""

    @staticmethod
    def _set_widget_text(widget, text):
        rendered = apply_bidi_text(T(text)) if CURRENT_LANGUAGE == "ar" else T(text)

        try:
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", rendered)
                widget.configure(justify="right" if CURRENT_LANGUAGE == "ar" else "left")
                return

            widget.configure(text=rendered)
            try:
                widget.configure(anchor="e" if CURRENT_LANGUAGE == "ar" else "w")
            except Exception:
                pass
            try:
                widget.configure(justify="right" if CURRENT_LANGUAGE == "ar" else "left")
            except Exception:
                pass
        except Exception:
            pass

    def refresh_client_combo(self):
        self.client_manager.load_clients()
        names = [client.name for client in self.client_manager.clients]
        values = ["<New Client>"] + names
        self.client_combo.configure(values=values)
        current_value = self.client_name_var.get()
        if current_value in values:
            self.client_combo.set(current_value)
        else:
            self.client_combo.set("<New Client>")

    def refresh_display(self):
        if self.plan is None:
            self.all_tasks_box.delete(0, tk.END)
            self.pending_tasks_box.delete(0, tk.END)
            self.all_tasks_box.insert(tk.END, T("No client selected"))
            self.pending_tasks_box.insert(tk.END, T("No pending tasks"))
            return

        self.all_tasks_box.delete(0, tk.END)
        self.pending_tasks_box.delete(0, tk.END)
        for index, task in enumerate(self.plan.all_tasks, start=1):
            self.all_tasks_box.insert(tk.END, self.format_task_entry(task, number=index))
        if not self.plan.pending_tasks:
            self.pending_tasks_box.insert(tk.END, T("No pending tasks"))
        else:
            for index, task in enumerate(self.plan.pending_tasks, start=1):
                self.pending_tasks_box.insert(tk.END, self.format_task_entry(task, number=index))

        self.progress_var.set(f"{self.plan.progress}%")
        self.progress_bar["value"] = self.plan.progress

    def clear_client_form(self):
        self.plan = None
        self.client_name_var.set("<New Client>")
        self.contact_var.set("")
        self.business_var.set("")
        self.shop_number_var.set("")
        self.address_var.set("")
        self.electrical_meter_var.set("")
        self.email_var.set("")
        self.total_tasks_var.set("0")
        self.progress_var.set("0%")
        self.progress_bar["value"] = 0
        self.all_tasks_box.delete(0, tk.END)
        self.pending_tasks_box.delete(0, tk.END)
        self.all_tasks_box.insert(tk.END, T("No client selected"))
        self.pending_tasks_box.insert(tk.END, T("No pending tasks"))

    def refresh_lang_ui(self):
        for widget, original_text in getattr(self, "translatable_labels", []):
            try:
                self._set_widget_text(widget, original_text)
            except Exception:
                pass

        if hasattr(self, "review_text"):
            try:
                self.review_text.configure(justify="right" if CURRENT_LANGUAGE == "ar" else "left")
            except Exception:
                pass

    @staticmethod
    def format_task_entry(task, number=None):
        text = str(task).strip()
        if number is not None:
            return f"{number}. {text}" if text else f"{number}."
        return text if text else ""
