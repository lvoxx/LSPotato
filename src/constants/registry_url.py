from ..constants.app_const import (
    REGISTRY_USER,
    REGISTRY_REPO_NAME,
    REGISTRY_FILE,
    REGISTRY_BRANCH,
    GIT_RAW_CONTENT_URL,
    CREATOR_REGISTRY_FILE,
)


def getRegistryDLUrl(registry_path) -> str:
    url = f"{GIT_RAW_CONTENT_URL}/{REGISTRY_USER}/{REGISTRY_REPO_NAME}/{REGISTRY_BRANCH}/{registry_path}/{REGISTRY_FILE}"
    return url


def getCreatorRegistrryDLURL(user, repo, branch="main") -> str:
    url = f"{GIT_RAW_CONTENT_URL}/{user}/{repo}/{branch}/{CREATOR_REGISTRY_FILE}"
    return url