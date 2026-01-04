import bpy  # type: ignore
from ...utils.get_blender_things import get_2remove_collections, get_2remove_libs
from ...utils.logger import get_logger

logger = get_logger("FindLSCherry")


def clean_linked_libraries(new_version: str) -> dict:
    """
    Xóa các linked libraries cũ
    
    Args:
        new_version: Version mới
        
    Returns:
        dict: {
            'removed_count': int,
            'message': str
        }
        
    Raises:
        Exception: Khi xóa libraries thất bại
    """
    to_remove_libs = get_2remove_libs(new_version)
    
    if not to_remove_libs:
        message = "No old linked libraries to remove"
        logger.info(message)
        return {
            'removed_count': 0,
            'message': message
        }
    
    try:
        count = len(to_remove_libs)
        for lib in to_remove_libs:
            bpy.data.libraries.remove(lib)
        message = f"Removed {count} linked library(ies)"
        logger.info(message)
        return {
            'removed_count': count,
            'message': message
        }
    except Exception as e:
        logger.error(f"Failed to remove linked libraries: {str(e)}")
        raise


def clean_lscherry_collection(new_version: str) -> dict:
    """
    Xóa các LSCherry collections cũ
    
    Args:
        new_version: Version mới
        
    Returns:
        dict: {
            'removed_name': str,
            'removed_count': int,
            'message': str
        }
        
    Raises:
        Exception: Khi xóa collection thất bại
    """
    to_remove_cols = get_2remove_collections(new_version)
    
    if not to_remove_cols:
        message = "No old collections to remove"
        logger.info(message)
        return {
            'removed_name': None,
            'removed_count': 0,
            'message': message
        }
    
    removed_name = to_remove_cols[0].name
    
    try:
        count = len(to_remove_cols)
        for col in to_remove_cols:
            del_col = col.name
            bpy.data.collections.remove(col)
            logger.info(f"Removed LSCherry collection {del_col}")
        
        message = f"Removed {count} collection(s): {removed_name}"
        return {
            'removed_name': removed_name,
            'removed_count': count,
            'message': message
        }
    except Exception as e:
        logger.error(f"Failed to remove collections: {str(e)}")
        raise


def clean_lscherry(new_version: str) -> dict:
    """
    Dọn dẹp LSCherry cũ (libraries và collections)
    
    Args:
        new_version: Version mới
        
    Returns:
        dict: {
            'libraries': dict,
            'collections': dict,
            'message': str
        }
        
    Raises:
        Exception: Khi dọn dẹp thất bại
    """
    libs_result = clean_linked_libraries(new_version)
    cols_result = clean_lscherry_collection(new_version)
    
    total_removed = libs_result['removed_count'] + cols_result['removed_count']
    
    if total_removed == 0:
        message = "Nothing to clean"
    else:
        parts = []
        if libs_result['removed_count'] > 0:
            parts.append(f"{libs_result['removed_count']} library(ies)")
        if cols_result['removed_count'] > 0:
            parts.append(f"{cols_result['removed_count']} collection(s)")
        message = f"Cleaned: {', '.join(parts)}"
    
    logger.info(message)
    
    return {
        'libraries': libs_result,
        'collections': cols_result,
        'message': message
    }