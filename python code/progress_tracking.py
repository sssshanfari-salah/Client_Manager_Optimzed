# Lightweight task-tracking model used to track a client's milestone progress.
# This module stores tasks, pending work, and the calculated progress percentage.
from clients_management import Client


class plan:
    # Shared dictionary used to keep progress data available across the app.
    Clients_progress = {}

    def __init__(self, client: Client, all_tasks=None):
        # Store the client and initialize the list of all tasks plus the currently pending ones.
        self.client = client
        self.Client_name = client.name
        self.all_tasks = list(all_tasks) if all_tasks is not None else []
        self.pending_tasks = list(self.all_tasks)
        self.progress = 0
        self.refresh_progress()

    # Recalculate completion percentage based on how many tasks still remain.
    def refresh_progress(self):
        if not self.all_tasks:
            self.progress = 100
            return self.progress

        remaining_tasks = len(self.pending_tasks)
        completed_tasks = len(self.all_tasks) - remaining_tasks
        self.progress = round((completed_tasks / len(self.all_tasks)) * 100)
        return self.progress

    # Add a new task and mark it as pending.
    def add_pending_task(self, task):
        self.all_tasks.append(task)
        self.pending_tasks.append(task)
        self.refresh_progress()
        self.update_clients_progress()

    # Mark a task as complete by removing it from the pending list.
    def complete_task(self, task):
        if task in self.pending_tasks:
            self.pending_tasks.remove(task)
        self.refresh_progress()
        self.update_clients_progress()

    # Convert the object into a JSON-friendly dictionary for persistence and reporting.
    def to_dict(self):
        return {
            "client_name": self.Client_name,
            "progress": self.progress,
            "pending_tasks": list(self.pending_tasks),
            "all_tasks": list(self.all_tasks),
        }

    # Save the current progress snapshot into the shared class-level tracker.
    def update_clients_progress(self):
        self.refresh_progress()
        plan.Clients_progress[self.client.name] = self.to_dict()

    # Return a text-based progress bar for simple terminal output or user-facing summaries.
    def progress_color(self):
        width = 30
        filled = int((self.progress / 100) * width)
        bar = "█" * filled + " " * (width - filled)
        return f"|{bar}| {self.progress}%\nPending tasks: {len(self.pending_tasks)}"
