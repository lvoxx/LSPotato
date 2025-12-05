import os
import bpy  # type: ignore
from .lscherry_path import get_version_path, get_blend_file
from .download_and_extract import download_and_extract


def repair_broken_version(self, version):
    """Repair a broken LSCherry version by re-downloading and extracting it"""
    # Re-download and extract the version
    return download_and_extract(self, version)


def is_valid_library(lib):
    """Kiểm tra xem library có hợp lệ không."""
    try:
        # Kiểm tra filepath tồn tại và là tệp .blend
        # IMPORTANT: Sử dụng bpy.path.abspath để resolve relative paths
        abs_path = bpy.path.abspath(lib.filepath)
        return os.path.exists(abs_path) and abs_path.endswith(".blend")
    except:
        return False


def is_lscherry_library(lib):
    """Kiểm tra xem library có phải là LSCherry không dựa vào tên file."""
    try:
        # Lấy tên file từ đường dẫn
        filename = os.path.basename(bpy.path.abspath(lib.filepath))
        # Kiểm tra xem có phải là LS Cherry.blend hoặc LS Cherry.local.blend không
        return filename in ["LS Cherry.blend", "LS Cherry.local.blend"]
    except:
        return False


def get_broken_libraries():
    """Trả về danh sách các LSCherry libraries bị hỏng."""
    broken_libs = []
    for lib in bpy.data.libraries:
        # Chỉ xét các library có tên file là LSCherry
        if is_lscherry_library(lib):
            if not is_valid_library(lib):
                broken_libs.append(lib)
    return broken_libs


def extract_version_from_collection(collection_name):
    """Extract version từ collection name (LSCherry-1.2.1 -> 1.2.1)"""
    return collection_name.replace("LSCherry-", "")


def repair_lscherry_collection(self):
    """
    Tìm collection LSCherry duy nhất và repair các broken libraries
    """
    # Tìm collection LSCherry duy nhất
    lscherry_collection = None
    for coll in bpy.data.collections:
        if coll.name.startswith("LSCherry-"):
            lscherry_collection = coll
            break

    if not lscherry_collection:
        self.report({"INFO"}, "No LSCherry collection found")
        return {"FINISHED"}

    # Extract version từ collection name (LSCherry-1.2.1 -> 1.2.1)
    version = extract_version_from_collection(lscherry_collection.name)
    
    # Lấy danh sách broken libraries
    broken_libs = get_broken_libraries()
    if not broken_libs:
        self.report({"INFO"}, "No broken LSCherry libraries found")
        return {"FINISHED"}

    try:
        # Kiểm tra và đảm bảo version đã được download
        version_path = get_version_path(version)
        if not os.path.exists(version_path):
            self.report({"INFO"}, f"Version {version} not found locally, downloading...")
            version_path = download_and_extract(self, version)
            
        if not version_path or not os.path.exists(version_path):
            self.report({"ERROR"}, f"Failed to get version {version}")
            return {"CANCELLED"}

        # Lấy đường dẫn blend file chính xác
        correct_blend_path = get_blend_file(version)
        if not os.path.exists(correct_blend_path):
            self.report({"ERROR"}, f"Blend file not found: {correct_blend_path}")
            return {"CANCELLED"}

        relocated_libs = []

        # Repair từng broken library
        for lib in broken_libs:
            old_path = lib.filepath
            
            # Set đường dẫn mới (absolute path)
            lib.filepath = correct_blend_path
            
            self.report({"INFO"}, f"Relocated {lib.name}: {old_path} -> {correct_blend_path}")
            relocated_libs.append(lib.name)

        # Reload tất cả relocated libraries
        for lib_name in relocated_libs:
            lib = bpy.data.libraries.get(lib_name)
            if lib:
                try:
                    lib.reload()
                    self.report({"INFO"}, f"Reloaded {lib_name}")
                except Exception as e:
                    self.report({"ERROR"}, f"Failed to reload {lib_name}: {e}")
                    return {"CANCELLED"}

        self.report({"INFO"}, f"Successfully repaired {len(relocated_libs)} LSCherry library(ies) for version {version}")
        return {"FINISHED"}

    except Exception as e:
        self.report({"ERROR"}, f"Error repairing version {version}: {e}")
        return {"CANCELLED"}


def count_broken_libraries():
    """Đếm số LSCherry libraries có đường dẫn bị hỏng."""
    return len(get_broken_libraries())