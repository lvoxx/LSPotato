import os
import bpy  # type: ignore
from .lscherry_path import get_version_path, get_blend_file
from .download_and_extract import download_and_extract
from ...exception.model.lspotato_exceptions import (
    LinkingException,
    ReleaseNotFoundException,
)
from ...utils.logger import get_logger

logger = get_logger("FindLSCherry")


def is_valid_library(lib) -> bool:
    """
    Check if library is valid

    Args:
        lib: Blender library object

    Returns:
        bool: True if library is valid
    """
    try:
        abs_path = bpy.path.abspath(lib.filepath)
        return os.path.exists(abs_path) and abs_path.endswith(".blend")
    except:
        return False


def is_lscherry_library(lib) -> bool:
    """
    Check if library is LSCherry

    Args:
        lib: Blender library object

    Returns:
        bool: True if is LSCherry library
    """
    try:
        filename = os.path.basename(bpy.path.abspath(lib.filepath))
        return filename in ["LS Cherry.blend", "LS Cherry.local.blend"]
    except:
        return False


def get_broken_libraries() -> list:
    """
    Get list of broken LSCherry libraries

    Returns:
        list: List of broken libraries
    """
    broken_libs = []
    for lib in bpy.data.libraries:
        if is_lscherry_library(lib):
            if not is_valid_library(lib):
                broken_libs.append(lib)
    return broken_libs


def extract_version_from_collection(collection_name: str) -> str:
    """
    Extract version from collection name

    Args:
        collection_name: Collection name (LSCherry-1.2.1)

    Returns:
        str: Version (1.2.1)
    """
    return collection_name.replace("LSCherry-", "")


def repair_lscherry_collection() -> dict:
    """
    Find and repair single LSCherry collection

    Returns:
        dict: Repair result with keys 'repaired_count' and 'version'

    Raises:
        ReleaseNotFoundException: When version not found
        LinkingException: When repair fails
    """
    # Find single LSCherry collection
    lscherry_collection = None
    for coll in bpy.data.collections:
        if coll.name.startswith("LSCherry-"):
            lscherry_collection = coll
            break

    if not lscherry_collection:
        logger.info("No LSCherry collection found")
        return {"repaired_count": 0, "version": None}

    # Extract version from collection name
    version = extract_version_from_collection(lscherry_collection.name)

    # Get list of broken libraries
    broken_libs = get_broken_libraries()
    if not broken_libs:
        logger.info("No broken LSCherry libraries found")
        return {"repaired_count": 0, "version": version}

    # Check and ensure version is downloaded
    version_path = get_version_path(version)
    if not os.path.exists(version_path):
        logger.info(f"Version {version} not found locally, downloading...")
        try:
            version_path = download_and_extract(version)
        except Exception as e:
            raise ReleaseNotFoundException(version=version, repo="LSCherry")

    if not version_path or not os.path.exists(version_path):
        raise ReleaseNotFoundException(version=version, repo="LSCherry")

    # Get correct blend file path
    correct_blend_path = get_blend_file(version)
    if not os.path.exists(correct_blend_path):
        raise LinkingException(
            library_path=correct_blend_path,
            reason=f"Blend file not found after download",
        )

    relocated_libs = []

    # Repair each broken library
    try:
        for lib in broken_libs:
            old_path = lib.filepath

            # Set new path (absolute path)
            lib.filepath = correct_blend_path

            logger.info(f"Relocated {lib.name}: {old_path} -> {correct_blend_path}")
            relocated_libs.append(lib.name)

        # Reload all relocated libraries
        for lib_name in relocated_libs:
            lib = bpy.data.libraries.get(lib_name)
            if lib:
                try:
                    lib.reload()
                    logger.info(f"Reloaded {lib_name}")
                except Exception as e:
                    raise LinkingException(
                        library_path=correct_blend_path,
                        reason=f"Failed to reload {lib_name}: {str(e)}",
                    )

        logger.info(
            f"Successfully repaired {len(relocated_libs)} LSCherry library(ies) for version {version}"
        )
        return {"repaired_count": len(relocated_libs), "version": version}

    except LinkingException:
        raise
    except Exception as e:
        raise LinkingException(
            library_path=correct_blend_path,
            reason=f"Error repairing libraries: {str(e)}",
        )


def count_broken_libraries() -> int:
    """
    Count LSCherry libraries with broken paths

    Returns:
        int: Number of broken libraries
    """
    return len(get_broken_libraries())
