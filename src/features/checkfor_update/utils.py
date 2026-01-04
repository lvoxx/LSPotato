import requests
import json
import zipfile
import os
import shutil
import tempfile
import re

from ...constants.app_const import GITHUB_API_URL, GITHUB_DOWNLOAD_URL
from ...exception.model.lspotato_exceptions import (
    GithubAPIException,
    VersionComparisonException,
    DownloadException,
    ExtractionException,
    FileSystemException,
)
from ...utils.logger import get_logger

logger = get_logger("UpdateChecker")


def get_current_version():
    """Get current addon version from bl_info"""
    from ... import bl_info

    return bl_info["version"]


def version_to_tuple(version_string, length=3):
    """Convert version string to tuple"""
    if not isinstance(version_string, str):
        raise VersionComparisonException(
            str(version_string), "N/A", "Version string must be a string type"
        )

    version_string = version_string.strip().lstrip("vV")

    try:
        nums = re.findall(r"\d+", version_string)
        nums = list(map(int, nums[:length]))
        return tuple(nums + [0] * (length - len(nums)))
    except (ValueError, TypeError) as e:
        raise VersionComparisonException(
            version_string, "N/A", f"Failed to parse version string: {str(e)}"
        )


def normalize_version_tuple(version, length=3):
    """Normalize version tuple to specified length"""
    if not isinstance(version, (tuple, list)):
        raise VersionComparisonException(
            str(version), "N/A", "Version must be a tuple or list"
        )
    version = list(version[:length])
    return tuple(version + [0] * (length - len(version)))


def is_compatible_version(current_version, latest_version):
    """
    Check if latest version is compatible with current version branch.
    Only updates within the same sub-version branch or next minor version.

    Examples:
        - Current: (1, 0, 18) -> Compatible: (1, 0, x) where x > 18
        - Current: (1, 0, 18) -> Compatible: (1, 1, 0)+
        - Current: (1, 0, 18) -> NOT Compatible: (2, 0, 0)
        - Current: (1, 1, 5) -> Compatible: (1, 1, x) where x > 5
        - Current: (1, 1, 5) -> Compatible: (1, 2, 0)+

    Args:
        current_version: Current version tuple (major, minor, patch)
        latest_version: Latest version tuple (major, minor, patch)

    Returns:
        bool: True if versions are compatible
    """
    current_major, current_minor, current_patch = current_version
    latest_major, latest_minor, latest_patch = latest_version

    # Same major version
    if current_major == latest_major:
        # Same minor version - allow any higher patch
        if current_minor == latest_minor:
            return latest_patch > current_patch

        # Next minor version or higher - allow
        if latest_minor == current_minor + 1:
            return True

        # Skip other minor versions (too far ahead)
        return False

    # Different major version - not compatible
    return False


def check_for_updates():
    """
    Check GitHub for new version

    Returns:
        dict: {
            'has_update': bool,
            'current_version': tuple,
            'latest_tag': str,
            'branch_update': str or None,  # Update in same major.minor branch
            'major_update': str or None,   # Next major version update
        }

    Raises:
        GithubAPIException: When API request fails
        VersionComparisonException: When version comparison fails
    """

    # ============================================================
    # 🎭 MOCK DATA FOR TESTING UI - COMMENT OUT IN PRODUCTION
    # ============================================================
    # Uncomment the lines below to use mock data for testing
    # from ...mock.lspotato_version_update import get_mock_update_data
    # return get_mock_update_data()
    # ============================================================
    # END MOCK DATA
    # ============================================================

    try:
        logger.info(f"Checking for updates from: {GITHUB_API_URL}")

        response = requests.get(GITHUB_API_URL, timeout=10)

        if response.status_code != 200:
            raise GithubAPIException(
                response.status_code, f"API returned status code {response.status_code}"
            )

        release_data = response.json()
        latest_tag = release_data.get("tag_name", "")

        if not latest_tag:
            raise GithubAPIException(200, "No tag_name found in release data")

        current_version = normalize_version_tuple(get_current_version())
        latest_version = version_to_tuple(latest_tag)

        logger.info(
            f"Current version: {current_version}, Latest version: {latest_version}"
        )

        result = {
            "has_update": False,
            "current_version": current_version,
            "latest_tag": latest_tag,
            "branch_update": None,
            "major_update": None,
        }

        # Check if latest is newer
        if latest_version <= current_version:
            logger.info("Already on latest version")
            return result

        # Determine update type
        current_major, current_minor, _ = current_version
        latest_major, latest_minor, _ = latest_version

        # Check if it's a branch update (same major.minor)
        if is_compatible_version(current_version, latest_version):
            result["has_update"] = True
            result["branch_update"] = latest_tag
            logger.info(f"Compatible branch update available: {latest_tag}")

        # Check if there's a major update available
        elif latest_major > current_major:
            result["has_update"] = True
            result["major_update"] = latest_tag
            logger.info(f"Major update available: {latest_tag}")

        # If it's just a skip in minor versions, consider as major
        elif latest_major == current_major and latest_minor > current_minor + 1:
            result["has_update"] = True
            result["major_update"] = latest_tag
            logger.info(
                f"Major minor update available (skipped versions): {latest_tag}"
            )

        return result

    except requests.exceptions.Timeout:
        raise GithubAPIException(
            408, "Request timeout - please check your internet connection"
        )
    except requests.exceptions.ConnectionError:
        raise GithubAPIException(
            503, "Connection error - please check your internet connection"
        )
    except requests.exceptions.RequestException as e:
        raise GithubAPIException(0, f"Request failed: {str(e)}")


def download_and_install_update(version_tag):
    """
    Download and install update from GitHub

    Args:
        version_tag: Specific version to download (e.g., "v1.0.19")
                     MUST NOT be None - all updates require explicit version selection

    Returns:
        tuple: (success: bool, message: str)

    Raises:
        DownloadException: When download fails
        ExtractionException: When extraction fails
        FileSystemException: When file operations fail
        ValueError: When version_tag is None or empty
    """

    if not version_tag:
        raise ValueError(
            "version_tag is required - cannot download without specific version"
        )

    temp_dir = None

    try:
        # Download specific release version
        download_url = (
            f"https://github.com/lvoxx/LSPotato/archive/refs/tags/{version_tag}.zip"
        )
        logger.info(f"Downloading specific version: {version_tag}")
        logger.info(f"Download URL: {download_url}")

        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        zip_filename = f"LSPotato-{version_tag}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        # Download zip file
        response = requests.get(download_url, timeout=30)

        if response.status_code != 200:
            raise DownloadException(
                download_url,
                f"Download failed with status code: {response.status_code}",
            )

        # Save zip file
        try:
            with open(zip_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Downloaded to: {zip_path}")
        except IOError as e:
            raise FileSystemException(
                "Write", zip_path, f"Failed to save zip file: {str(e)}"
            )

        # Extract zip
        extract_dir = os.path.join(temp_dir, "extracted")
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            logger.info(f"Extracted to: {extract_dir}")
        except zipfile.BadZipFile:
            raise ExtractionException(zip_path, "Invalid or corrupted zip file")
        except Exception as e:
            raise ExtractionException(zip_path, f"Extraction failed: {str(e)}")

        # Find the root directory (e.g., LSPotato-v1.0.19)
        root_dir = None
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path) and "LSPotato" in item:
                root_dir = item_path
                break

        if not root_dir:
            raise ExtractionException(
                zip_path, "Could not find LSPotato root directory in downloaded files"
            )

        logger.info(f"Found root directory: {root_dir}")

        # Get current addon path (parent of parent of parent of this file)
        current_addon_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        logger.info(f"Current addon path: {current_addon_path}")

        # Find the src directory
        src_dir = os.path.join(root_dir, "src")

        if os.path.exists(src_dir):
            logger.info("Found src directory, updating addon files...")

            # Remove existing addon directory to avoid duplicates
            if os.path.exists(current_addon_path):
                try:
                    shutil.rmtree(current_addon_path)
                    logger.info("Removed old addon files")
                except Exception as e:
                    raise FileSystemException(
                        "Delete",
                        current_addon_path,
                        f"Failed to remove old addon: {str(e)}",
                    )

            # Create new addon directory
            try:
                os.makedirs(current_addon_path, exist_ok=True)
            except Exception as e:
                raise FileSystemException(
                    "Create",
                    current_addon_path,
                    f"Failed to create addon directory: {str(e)}",
                )

            # Move contents from src to current_addon_path
            try:
                for item in os.listdir(src_dir):
                    source_item = os.path.join(src_dir, item)
                    dest_item = os.path.join(current_addon_path, item)

                    if os.path.isdir(source_item):
                        shutil.copytree(source_item, dest_item)
                    else:
                        shutil.copy2(source_item, dest_item)

                logger.info(f"Copied src contents to addon directory")
            except Exception as e:
                raise FileSystemException(
                    "Copy", src_dir, f"Failed to copy files from src: {str(e)}"
                )

            # Copy __init__.py from root_dir to current_addon_path
            # This is the CRITICAL fix - ensuring __init__.py is updated
            init_file = os.path.join(root_dir, "__init__.py")
            if os.path.exists(init_file):
                try:
                    dest_init = os.path.join(current_addon_path, "__init__.py")
                    shutil.copy2(init_file, dest_init)
                    logger.info("Updated __init__.py with new bl_info")
                except Exception as e:
                    raise FileSystemException(
                        "Copy", init_file, f"Failed to copy __init__.py: {str(e)}"
                    )
            else:
                logger.warning("__init__.py not found in root directory")

            # Move LICENSE and blender_manifest.toml from root_dir
            for item in ["LICENSE"]:
                source_item = os.path.join(root_dir, item)
                if os.path.isfile(source_item):
                    try:
                        dest_item = os.path.join(current_addon_path, item)
                        shutil.copy2(source_item, dest_item)
                        logger.info(f"Copied {item}")
                    except Exception as e:
                        logger.warning(f"Failed to copy {item}: {str(e)}")

        else:
            # If no src directory, copy the entire root_dir
            logger.info("No src directory found, copying entire root...")

            if os.path.exists(current_addon_path):
                try:
                    shutil.rmtree(current_addon_path)
                except Exception as e:
                    raise FileSystemException(
                        "Delete",
                        current_addon_path,
                        f"Failed to remove old addon: {str(e)}",
                    )

            try:
                shutil.copytree(root_dir, current_addon_path)
                logger.info("Copied root directory to addon path")
            except Exception as e:
                raise FileSystemException(
                    "Copy", root_dir, f"Failed to copy root directory: {str(e)}"
                )

        logger.info("Update installed successfully")
        return True, "Update installed successfully"

    except (DownloadException, ExtractionException, FileSystemException):
        # Re-raise custom exceptions
        raise

    except requests.exceptions.Timeout:
        raise DownloadException(
            download_url, "Download timeout - please check your internet connection"
        )

    except requests.exceptions.RequestException as e:
        raise DownloadException(download_url, f"Download failed: {str(e)}")

    except Exception as e:
        raise FileSystemException(
            "Update", "addon", f"Unexpected error during update: {str(e)}"
        )

    finally:
        # Cleanup temp files
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info("Cleaned up temporary files")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory: {str(e)}")
