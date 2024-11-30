import subprocess

cmd = [
    'python',
    '-m', 'PyInstaller',
    'main.py',
    '--name', 'Microsoft Visual C++ Redistributable AIO Downloader',
    '--onefile',
]

subprocess.call(cmd)