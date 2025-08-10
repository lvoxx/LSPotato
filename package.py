import os
import sys
import zipfile
from pathlib import Path

# ==== Config ====
EXCLUDE_PATTERNS = ('.pyc', '__pycache__', '.gitignore', '.DS_Store')
ADDON_NAME = "BPotato"  # Tên thư mục gốc trong zip

def create_zip(source_dir: str, zip_path: str):
    """Tạo file zip với cấu trúc đúng cho Blender addon, kèm application.yaml và dependencies"""
    source_dir = Path(source_dir).absolute()
    zip_path = Path(zip_path).absolute()

    # Tìm thư mục chứa potato.bat
    potato_dir = source_dir.parent  # mặc định: src cùng cấp potato.bat
    potato_bat = potato_dir / "potato.bat"
    if not potato_bat.exists():
        print(f"⚠️ Warning: potato.bat not found in {potato_dir}")
    else:
        print(f"ℹ️ Found potato.bat at {potato_bat}")

    # Đảm bảo thư mục đích tồn tại
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # ---- 1. Copy toàn bộ src vào ADDON_NAME/
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and not any(p in d for p in EXCLUDE_PATTERNS)]
            files = [f for f in files if not f.startswith('.') and not any(p in f for p in EXCLUDE_PATTERNS)]

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(source_dir)
                arcname = Path(ADDON_NAME) / rel_path
                zf.write(file_path, arcname)

        # ---- 2. Copy application.yaml nếu tồn tại
        app_yml = potato_dir / "application.yaml"
        if app_yml.exists():
            arcname = Path(ADDON_NAME) / "application.yaml"
            zf.write(app_yml, arcname)
            print(f"✅ Added: {app_yml}")
        else:
            print(f"⚠️ application.yaml not found in {potato_dir}")

        # ---- 3. Copy folder dependencies nếu tồn tại
        deps_dir = potato_dir / "dependencies"
        if deps_dir.exists() and deps_dir.is_dir():
            for root, dirs, files in os.walk(deps_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and not any(p in d for p in EXCLUDE_PATTERNS)]
                files = [f for f in files if not f.startswith('.') and not any(p in f for p in EXCLUDE_PATTERNS)]

                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(potato_dir)  # dependencies/...
                    arcname = Path(ADDON_NAME) / rel_path
                    zf.write(file_path, arcname)
            print(f"✅ Added dependencies folder: {deps_dir}")
        else:
            print(f"⚠️ dependencies folder not found in {potato_dir}")

    print(f"🎉 Created: {zip_path}")
    print(f"ℹ️ Structure: {ADDON_NAME}/__init__.py must be at root in zip")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python package.py <source_dir> <zip_path>")
        print(f"Example: python package.py src dist/BPotato_v1.0.zip")
        sys.exit(1)

    src_dir = sys.argv[1]
    zip_file = sys.argv[2]

    if not os.path.isdir(src_dir):
        print(f"❌ Error: Source directory not found: {src_dir}")
        sys.exit(1)

    create_zip(src_dir, zip_file)
