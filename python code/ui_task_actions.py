"""Task-management actions for the main application window."""

import tkinter as tk
from tkinter import messagebox

from business_logic import Plan
from translations import T


class TaskManagementMixin:
    """Methods for task operations and progress updates."""

    def add_new_task(self):
        if self.plan is None:
            messagebox.showwarning(T("No client plan"), T("Create a client plan first."))
            return

        task_text = self.new_task_var.get().strip()
        if not task_text:
            task_text = "New Task"
        self.plan.add_pending_task(task_text)
        self.new_task_var.set("")
        self.refresh_display()

    def complete_selected_task(self):
        if self.plan is None:
            return
        selected = self.pending_tasks_box.curselection()
        if not selected:
            messagebox.showwarning(T("No task selected"), T("Select a task from the pending list."))
            return
        task = self.pending_tasks_box.get(selected[0]).split(". ", 1)[-1]
        self.plan.complete_task(task)
        self.refresh_display()
