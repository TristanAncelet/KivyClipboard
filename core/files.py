from pathlib import Path

home_dir = Path.home()
data_dir = home_dir / ".data"
clipboard_file = data_dir / "clipboard.json"

if not data_dir.exists():
    data_dir.mkdir()

if not clipboard_file.exists():
    clipboard_file.touch()

