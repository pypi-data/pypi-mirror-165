import zipfile
import platform
import os
import requests
import shutil
import subprocess
import re

from pathlib import Path


class DownloadBitwarden(object):
    """
    Purpose of this class is only downloading of BitWarden CLI
    """

    @staticmethod
    def download_site(platform):
        """Downloads cli binary from official web site."""
        bitwarden_url = f"https://vault.bitwarden.com/download/?app=cli&platform={platform}"

        r = requests.get(
            bitwarden_url,
            allow_redirects=True,
        )

        return r

    @staticmethod
    def download_github(platform):
        """Downloads cli binary from github releases page."""
        # setup for alternative download url
        # Step 1: make a request to get a current CLI tool version
        fetch_url = "https://github.com/bitwarden/clients/releases?page="
        link_pattern = r"<a href=\"(\/bitwarden/[a-z\/]+/cli-v[\d\.]+\/bw-{}-\d+\.\d+\.\d+\.zip)\"".format(platform)
        r = None

        for i in range(1, 5):
            r0 = requests.get(fetch_url + str(i), allow_redirects=True)
            direct_link = re.search(link_pattern, r0.text, re.IGNORECASE | re.MULTILINE)
            if len(direct_link.groups()) == 1:
                alternate_download_link = f"https://github.com{direct_link.groups()[0]}"
                print(f"\nDownloading Bitwarden CLI '{direct_link.groups()[0].split('/')[-1]}'")
                r = requests.get(
                    alternate_download_link,
                    allow_redirects=True,
                )
                break

        return r

    @staticmethod
    def download_local(platform, path_to_zip_file):
        """Downloads cli binary from localy storred files coming with package."""
        filepath = os.path.join(os.path.dirname(__file__), "binaries", f"bw-{platform}.zip")
        shutil.copy(filepath, path_to_zip_file)

    @staticmethod
    def download_bitwarden(source="local"):
        """
        Static method that does downloading of CLI corresponding to execution env
        Available environments:
          - linux
          - macos
          - windows

        By default tries to download the cli binary using order source:
          - site
          - github
          - local
        """
        sources = ["default", "site", "github", "local"]
        if source not in sources:
            raise Exception(f"Unknown download source {source}! Available sources: default, site, github, local")

        platforms = {"linux": "linux", "darwin": "macos", "windows": "windows"}
        p = platforms[platform.system().lower()]

        cwd = os.getcwd()
        path_to_exe_file = ""
        moved = False
        r = None

        print(f"\nDownloading bitwarden CLI binary for {p} from {source}...\n")

        path_to_zip_file = os.path.join(cwd, "bitwarden.zip")

        if source == "default":
            r = DownloadBitwarden.download_site(p)

            if r.status_code != 200:
                r = DownloadBitwarden.download_github(p)

            if r.status_code != 200:
                DownloadBitwarden.download_local(p, path_to_zip_file)

        if source == "site":
            r = DownloadBitwarden.download_site(p)

        if source == "github":
            r = DownloadBitwarden.download_github(p)

        if source == "local":
            DownloadBitwarden.download_local(p, path_to_zip_file)

        if r:
            if r.status_code == 200:
                open(path_to_zip_file, "wb").write(r.content)

        with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
            zip_ref.extract(zip_ref.namelist()[0], cwd)
            path_to_exe_file = os.path.join(cwd, zip_ref.namelist()[0])

        print(f"\nSuccessfully extracted BitWarden binary to {path_to_exe_file}\n")

        Path(path_to_zip_file).unlink(missing_ok=True)

        if platform.system().lower() == "windows":
            environment_path_var: list = os.getenv("PATH").split(";")
            file_name_with_extension: str = "bw.exe"
        else:
            environment_path_var: list = os.getenv("PATH").split(":")[1:]
            file_name_with_extension: str = "bw"

        # Try to move CLI binary to PATH
        for path_dir in environment_path_var:
            try:
                Path(path_to_exe_file).rename(os.path.join(path_dir, file_name_with_extension))
                path_to_exe_file = os.path.join(path_dir, file_name_with_extension)
                moved = True
                break
            except Exception:
                continue

        if moved:
            print(f"\nSuccessfully moved BitWarden binary to {path_to_exe_file}\n")
        else:
            print(f"\nFailed to move BitWarden binary. Current path is {path_to_exe_file}\n")

        if platform.system().lower() != "windows":
            subprocess.run(["chmod", "+x", path_to_exe_file], capture_output=True, text=True)

        return path_to_exe_file
