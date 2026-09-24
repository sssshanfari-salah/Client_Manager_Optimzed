# Utility script that keeps a project document copy synchronized between source and target locations.
# This is mainly used to mirror content when the app or packaging workflow expects a stable docs file.
from __future__ import annotations

import hashlib
import time
from pathlib import Path

# Resolve the project root and the staged docs path used by the app.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = PROJECT_ROOT / "data" / "docs"
SOURCE = DOCS_DIR / "documents.txt"
TARGET = DOCS_DIR / "documents.txt"


# Copy the current document data once if the source and target differ.
def sync_once() -> bool:
    if not SOURCE.exists():
        print(f"Source file not found: {SOURCE}")
        return False

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    source_bytes = SOURCE.read_bytes()
    if TARGET.exists() and TARGET.read_bytes() == source_bytes:
        return True

    TARGET.write_bytes(source_bytes)
    print(f"Synced: {SOURCE} -> {TARGET}")
    return True


# Watch the source file for changes and sync it repeatedly.
def main() -> None:
    print(f"Watching for changes...\nSource: {SOURCE}\nTarget: {TARGET}")
    last_hash = None

    while True:
        if SOURCE.exists():
            source_bytes = SOURCE.read_bytes()
            current_hash = hashlib.sha256(source_bytes).hexdigest()
            if last_hash is None or current_hash != last_hash:
                last_hash = current_hash
                sync_once()
        time.sleep(2)


# Run a final sync immediately when the script starts, then begin monitoring.
if __name__ == "__main__":
    sync_once()
    main()
