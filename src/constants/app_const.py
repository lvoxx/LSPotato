VERSION_REGEX = r"v\d+\.\d+\.\d+"
LSCHERRY_COL_REGEX = r"^LSCherry-(\d+\.\d+\.\d+(?:\.\d+)?)$"
LSCHERRY_ROOT = "https://github.com/lvoxx/LSCherry"
LSCHERRY_DL_URL = LSCHERRY_ROOT + "/releases/download"

GIT_RAW_CONTENT_URL="https://raw.githubusercontent.com"

# LSCherry dependencies info
LSCHERRY_ROOT_FOLDER = "LS Cherry"
LSCHERRY_FILE = "LS Cherry"
LSCHERRY_FILE_WITH_EXTENSION = f"{LSCHERRY_FILE}.local.blend"
CHERRY_OBJECT = "Cherry"
LSCHERRY_COLLECTION_COLOR = "COLOR_01" # Red color

LSCHERRY_PROVIDER = "Core.LSCherryProvider"

# GitHub repo info
GITHUB_USER = "lvoxx"
GITHUB_REPO = "LSPotato"
GITHUB_API_URL = (
    f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
)
GITHUB_DOWNLOAD_URL = (
    f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/main.zip"
)

# LSRegistry
REGISTRY_USER = "lvoxx"
REGISTRY_REPO_NAME = "LSRegistry"
REGISTRY_BRANCH = "main"
REGISTRY_FILE = "registry.yaml"
CREATOR_REGISTRY_FILE = "registry.ls.yaml"
REGISTRY_COLLECTION_COLOR= "COLOR_05"  # Blue color
