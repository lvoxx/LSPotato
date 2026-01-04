import os
import shutil
import zipfile
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError
from ...constants.lscherry_version import version_urls
from .lscherry_path import get_lscherry_path, get_version_path
from ...exception.model.lspotato_exceptions import (
    DownloadException,
    ExtractionException,
    ReleaseNotFoundException,
)
from ...utils.logger import get_logger

logger = get_logger("FindLSCherry")


def download_and_extract(version: str) -> dict:
    """
    Download và extract LSCherry version

    Args:
        version: Version cần download

    Returns:
        dict: {
            'extract_path': str,
            'was_downloaded': bool,
            'message': str
        }

    Raises:
        ReleaseNotFoundException: Khi không tìm thấy URL cho version
        DownloadException: Khi download thất bại
        ExtractionException: Khi extract thất bại
    """
    lscherry_dir = get_lscherry_path()
    extract_path = get_version_path(version)

    # Check if version already exists
    if os.path.exists(extract_path):
        message = f"Version {version} found locally, using existing version"
        logger.info(message)
        return {
            "extract_path": extract_path,
            "was_downloaded": False,
            "message": message,
        }

    os.makedirs(extract_path, exist_ok=True)

    # Get URL from version_urls
    url = version_urls.get(version, "")
    if not url:
        raise ReleaseNotFoundException(version=version, repo="LSCherry")

    logger.info(f"Found version {version} at {url}")

    # Always expect .zip
    archive_path = os.path.join(lscherry_dir, f"LSCherry-{version}.zip")

    # Download file
    try:
        urlretrieve(url, archive_path)
        logger.info(f"Downloaded to {archive_path}")
    except HTTPError as e:
        raise DownloadException(url=url, reason=f"HTTP Error {e.code}: {e.reason}")
    except URLError as e:
        raise DownloadException(url=url, reason=f"URL Error: {e.reason}")
    except Exception as e:
        raise DownloadException(url=url, reason=f"Download failed: {str(e)}")

    # Extract file
    try:
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        raise ExtractionException(
            zip_path=archive_path, reason="File is not a valid zip archive"
        )
    except PermissionError:
        raise ExtractionException(
            zip_path=archive_path, reason="Permission denied when extracting"
        )
    except Exception as e:
        raise ExtractionException(
            zip_path=archive_path, reason=f"Extraction failed: {str(e)}"
        )
    finally:
        # Clean up archive
        if os.path.exists(archive_path):
            try:
                os.remove(archive_path)
            except:
                logger.warning(f"Failed to remove archive: {archive_path}")

    # Fix double-nesting: if extract_path contains a single folder, move its content up
    try:
        items = os.listdir(extract_path)
        if len(items) == 1:
            inner_dir = os.path.join(extract_path, items[0])
            if os.path.isdir(inner_dir):
                # Move everything inside inner_dir up one level
                for sub in os.listdir(inner_dir):
                    shutil.move(os.path.join(inner_dir, sub), extract_path)
                shutil.rmtree(inner_dir)
    except Exception as e:
        logger.warning(f"Failed to fix double-nesting: {str(e)}")

    message = f"Successfully downloaded and extracted version {version}"
    logger.info(message)

    return {"extract_path": extract_path, "was_downloaded": True, "message": message}
