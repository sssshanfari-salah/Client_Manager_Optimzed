# Lightweight validation script for the UI layer.
# It confirms that the main Tkinter file parses correctly and exposes the expected export actions.
import ast
import os
import sys
from pathlib import Path

# Adjust the root path if the project directory changes.
ROOT = Path(r"c:/Users/ssssh/OneDrive/Documents/Marketing_booster_ar")
UI_FILE = ROOT / "python code" / "clients_progress_ui.py"

# Confirm the UI file is syntactically valid before importing it.
print("Checking UI syntax...")
source = UI_FILE.read_text(encoding="utf-8")
ast.parse(source)
print("UI syntax OK")

# Import the application module and validate the expected public entry points and output folders.
sys.path.insert(0, str(ROOT / "python code"))
import clients_progress_ui as ui

assert hasattr(ui.ProgressApp, "export_client_log"), "missing export_client_log"
assert hasattr(ui.ProgressApp, "export_task_log"), "missing export_task_log"
assert hasattr(ui.ProgressApp, "export_observation_log"), "missing export_observation_log"
assert ui.resolve_log_output_dir("clients_logs").name == "clients_logs"
assert ui.resolve_log_output_dir("tasks_logs").name == "tasks_logs"
assert ui.resolve_log_output_dir("observation_logs").name == "observation_logs"
print("UI actions and output folders OK")
