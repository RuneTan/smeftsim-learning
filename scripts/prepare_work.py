"""Copy tutorial inputs into a working directory, preserving the originals."""
from pathlib import Path
import shutil

base = Path(__file__).resolve().parents[1]
source = base / "tutorial/Material"
target = base / "work/Material"
target.mkdir(parents=True, exist_ok=True)
for item in source.iterdir():
    destination = target / item.name
    if destination.exists():
        continue
    if item.is_dir():
        shutil.copytree(item, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    else:
        shutil.copy2(item, destination)
for script in target.glob("*.sh"):
    # git on Windows may have converted LF to CRLF.
    script.write_text(script.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
print(target)
