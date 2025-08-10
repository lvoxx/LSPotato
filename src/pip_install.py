import subprocess
import sys

def ensure_package(package_name):
    """Cài đặt package nếu chưa tồn tại"""
    try:
        __import__(package_name)
    except ImportError:
        python_exe = sys.executable
        try:
            subprocess.check_call([python_exe, "-m", "ensurepip"])
        except Exception:
            pass  # ensurepip có thể đã cài rồi
        subprocess.check_call([python_exe, "-m", "pip", "install", package_name])
        __import__(package_name)

# Đảm bảo cài PyYAML
ensure_package("yaml")