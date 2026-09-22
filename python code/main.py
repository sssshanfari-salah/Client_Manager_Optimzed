# Application entry point.
# This file prepares the runtime path and starts the user interface for the client manager.
import sys
from pathlib import Path

# Ensure the source folder is importable when the app is launched from its project directory.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clients_progress_ui import safe_main

# Launch the main UI when the script is executed directly.
if __name__ == "__main__":
    safe_main()