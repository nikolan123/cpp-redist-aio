import os
import requests
import time
import tempfile
import ctypes
import sys

links = {
    "2015-latest": {
        "x64": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
        "x86": "https://aka.ms/vs/17/release/vc_redist.x86.exe"
    },
    "2013": {
        "x64": "https://aka.ms/highdpimfc2013x64enu",
        "x86": "https://aka.ms/highdpimfc2013x86enu"
    },
    "2012": {
        "x64": "https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x64.exe",
        "x86": "https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe"
    },
    "2010": {
        "x64": "https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x64.exe",
        "x86": "https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe"
    },
    "2008": {
        "x64": "https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x64.exe",
        "x86": "https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe"
    }
}

def main():
    os.system('cls')

    print("Microsoft Visual C++ Redistributable AIO Downloader")
    print("https://github.com/nikolan123/cpp-redist-aio")
    print("Licensed under GPLv3")
    print("*" * 51)

    download_install_all()

def dir_for_download():
    print("\nPreparing for installation")

    print("  - Checking internet connection")
    try:
        response = requests.get("https://download.microsoft.com", timeout=5)
    except Exception as e:
        print(f"  - Connection to download.microsoft.com was unsuccessful - {e}")
        exit()
    if response.status_code == 200:
        print("  - Connection to download.microsoft.com successful")
    else:
        print("  - Connection to download.microsoft.com was unsuccessful - non-200 returned")
        exit()

    print("  - Checking admin permissions")
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("  - Administrator permissions not present, press any key to request elevation")
        os.system("pause")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(f'"{arg}"' for arg in sys.argv), None, 1
        )
        sys.exit()
    else:
        print("  - All good")

    folder_name = f"{str(int(time.time()))}-cpp-downloader"
    temp_dir = tempfile.gettempdir()
    new_dir_path = os.path.join(temp_dir, folder_name)
    os.makedirs(new_dir_path)
    print(f"  - Created folder {new_dir_path}")

    return new_dir_path

def download_install_all():
    dl_dir = dir_for_download()
    for version, arch_links in links.items():
        print(f"\nDownloading files for {version}...")
        for arch, url in arch_links.items():
            print(f"  - Downloading {arch} from {url}")
            try:
                response = requests.get(url, stream=True)
                file_name = f"{version}_{arch}.exe"
                file_path = os.path.join(dl_dir, file_name)
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print(f"  - {file_name} downloaded successfully!")
            except Exception as e:
                print(f"  - Failed to download {arch}: {e}")
    print("\nAll versions downloaded!")

    downloaded_list = os.listdir(dl_dir)
    print(f"\n{len(downloaded_list)} files found")
    print(f"Installing all versions")
    for downloaded_file in downloaded_list:
        command_to_run = f"{os.path.join(dl_dir, downloaded_file)} /q /norestart"
        print(f"  - Running {command_to_run}")
        os.system(command_to_run)
        print("  - Done")

    print("*" * 51)
    print("All done!")

if __name__ == "__main__":
    main()