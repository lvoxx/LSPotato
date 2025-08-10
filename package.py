import os
import sys
import zipfile
from pathlib import Path

# ==== Config ====
EXCLUDE_PATTERNS = (".pyc", "__pycache__", ".gitignore", ".DS_Store")
ADDON_NAME = "BPotato"  # Tên thư mục gốc trong zip


def add_file_to_zip(zf: zipfile.ZipFile, file_path: Path, arcname: Path):
    """Thêm file vào zip với đường dẫn mong muốn"""
    if not file_path.exists():
        print(f"⚠ Skipped (not found): {file_path}")
        return
    zf.write(file_path, arcname)


def add_dir_to_zip(zf: zipfile.ZipFile, dir_path: Path, arc_base: Path):
    """Thêm toàn bộ thư mục vào zip"""
    if not dir_path.exists():
        print(f"⚠ Skipped folder (not found): {dir_path}")
        return
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and not any(p in d for p in EXCLUDE_PATTERNS)
        ]
        files = [
            f
            for f in files
            if not f.startswith(".") and not any(p in f for p in EXCLUDE_PATTERNS)
        ]
        for file in files:
            fpath = Path(root) / file
            rel_path = fpath.relative_to(dir_path)
            arcname = arc_base / rel_path
            zf.write(fpath, arcname)


def create_zip(source_dir: str, zip_path: str):
    """Tạo file zip với cấu trúc đúng cho Blender addon và copy thêm các file phụ"""
    source_dir = Path(source_dir).absolute()
    zip_path = Path(zip_path).absolute()

    # Đảm bảo thư mục đích tồn tại
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    # Lấy thư mục chứa potato.bat (cùng cấp với application.yml và dependencies)
    root_dir = source_dir.parent

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Nén toàn bộ addon vào thư mục ADDON_NAME/
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and not any(p in d for p in EXCLUDE_PATTERNS)
            ]
            files = [
                f
                for f in files
                if not f.startswith(".") and not any(p in f for p in EXCLUDE_PATTERNS)
            ]

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(source_dir)
                arcname = Path(ADDON_NAME) / rel_path
                zf.write(file_path, arcname)

        # 2. Copy thêm application.yml vào cùng cấp với potato.bat trong zip
        app_yml = root_dir / "application.yml"
        add_file_to_zip(zf, app_yml, Path("application.yml"))

        # 3. Copy thêm thư mục dependencies/
        deps_dir = root_dir / "dependencies"
        add_dir_to_zip(zf, deps_dir, Path("dependencies"))

    print(f"✅ Created: {zip_path}")
    print(f"Structure:")
    print(f"  {ADDON_NAME}/__init__.py (Blender addon)")
    print(f"  application.yml")
    print(f"  dependencies/")


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
