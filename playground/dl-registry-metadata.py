from pathlib import Path
import requests


def download_github_file_api(user, repo, path, token=None, branch="main", save_as=None):
    url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise Exception(f"Failed to fetch file: {r.status_code} - {r.text}")

    # Lấy thư mục chứa file .py đang chạy
    script_dir = Path(__file__).parent

    # Tên file mặc định
    save_as = save_as or path.split("/")[-1]

    # Gộp đường dẫn: thư mục script + tên file
    save_path = script_dir / save_as

    with open(save_path, "wb") as file:
        file.write(r.content)

    print(f"Downloaded to {save_path}")


# ---- GỌI HÀM ----
download_github_file_api(
    user="lvoxx",
    repo="LSRegistry",
    path="io/github/lvoxx/world-builder/metadata.yaml",
)
