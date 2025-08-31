VERSION_REGEX = r"v\d+\.\d+\.\d+"
LSCHERRY_COL_REGEX = r"^LSCherry-(\d+\.\d+\.\d+(?:\.\d+)?)$"
LSCHERRY_ROOT = "https://github.com/lvoxx/LSCherry"
LSCHERRY_TAGS = LSCHERRY_ROOT + "/archive/refs/tags"

# LSCherry dependencies info
LSCHERRY_FILE = "LS Cherry"
LSCHERRY_FILE_WITH_EXTENSION = f"{LSCHERRY_FILE}.blend"
CHERRY_OBJECT = "Cherry"

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
