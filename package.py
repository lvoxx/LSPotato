import os
import sys
import zipfile
from pathlib import Path

# ==== Config ====
EXCLUDE_PATTERNS = ('.pyc', '__pycache__', '.gitignore', '.DS_Store')
ADDON_NAME = "BPotato"  # Tên thư mục gốc trong zip

def create_zip(source_dir: str, zip_path: str):
    """Tạo file zip với cấu trúc đúng cho Blender addon"""
    source_dir = Path(source_dir).absolute()
    zip_path = Path(zip_path).absolute()

    # Đảm bảo thư mục đích tồn tại
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            # Lọc bỏ các thư mục/file không mong muốn
            dirs[:] = [d for d in dirs if not d.startswith('.') and not any(p in d for p in EXCLUDE_PATTERNS)]
            files = [f for f in files if not f.startswith('.') and not any(p in f for p in EXCLUDE_PATTERNS)]

            for file in files:
                file_path = Path(root) / file
                
                # Tạo đường dẫn trong zip: ADDON_NAME/relative_path
                rel_path = file_path.relative_to(source_dir)
                arcname = str(Path(ADDON_NAME) / rel_path)
                
                zf.write(file_path, arcname)
    
    print(f"✅ Created: {zip_path}")
    print(f"Structure: {ADDON_NAME}/__init__.py must be at root in zip")

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