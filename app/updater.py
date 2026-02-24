# app/updater.py
import requests
from packaging.version import Version

CURRENT_VERSION = "2.0.0"

# After you create your GitHub repo, update this URL:
# https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/version.json
VERSION_CHECK_URL = "https://raw.githubusercontent.com/rakhul2003/test-update/main/version.json"


def get_current_version():
    return CURRENT_VERSION


def check_for_updates():
    """
    Returns update dict if new version available, None otherwise.
    Never crashes the app - silently fails on network errors.
    """
    try:
        response = requests.get(VERSION_CHECK_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        latest = data.get("version")
        if latest and Version(latest) > Version(CURRENT_VERSION):
            return data  # { version, download_url, release_notes }
        return None
    except Exception as e:
        print(f"[Updater] Check failed: {e}")
        return None


def download_installer(download_url: str, progress_callback=None) -> str:
    """
    Downloads installer to temp folder.
    Returns path to downloaded .exe
    """
    import tempfile
    import os

    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    downloaded = 0

    tmp_path = os.path.join(tempfile.gettempdir(), "test_update_installer.exe")

    with open(tmp_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if progress_callback and total:
                percent = int((downloaded / total) * 100)
                progress_callback(percent)

    return tmp_path


def launch_installer_and_exit(installer_path: str):
    """
    Runs the installer silently and quits the current app.
    /SILENT = shows progress but no questions
    /VERYSILENT = completely silent install
    """
    import subprocess
    import os
    subprocess.Popen([installer_path, "/SILENT"])
    os._exit(0)