from pathlib import Path
from datetime import datetime
import shutil
from database.database import DATABASE_PATH

def create_backup():
    folder=Path("backups"); folder.mkdir(exist_ok=True)
    target=folder/f"cafe_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(DATABASE_PATH,target)
    return str(target)

def list_backups():
    folder=Path("backups"); folder.mkdir(exist_ok=True)
    return sorted(folder.glob("*.db"),reverse=True)
