import os
import sys
import zipfile

# ==== Config ====
EXCLUDE_PATTERNS = ('.pyc', '__pycache__')

def create_zip(source_dir: str, zip_path: str):
    source_dir = os.path.abspath(source_dir)
    zip_path = os.path.abspath(zip_path)

    # Đảm bảo thư mục đích tồn tại
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            # Bỏ qua thư mục bị exclude
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in EXCLUDE_PATTERNS)]
            for file in files:
                if not any(pattern in file for pattern in EXCLUDE_PATTERNS):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zf.write(file_path, arcname)
    print(f"✅ Created: {zip_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python package.py <source_dir> <zip_path>")
        sys.exit(1)

    src_dir = sys.argv[1]
    zip_file = sys.argv[2]

    if not os.path.isdir(src_dir):
        print(f"❌ Error: Source directory not found: {src_dir}")
        sys.exit(1)

    create_zip(src_dir, zip_file)