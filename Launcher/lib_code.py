import requests
import subprocess
import threading
import time
import os
import sys

class LauncherLib:
    def __init__(self):
        self.repo_latest_release_url = "https://github.com/MaximalBrot-Inc/LiarsCards/releases/latest"
        #self.repo_latest_release_url = "https://github.com/astral-sh/uv/releases/latest"
    
    def get_version(self):
        try:
            res = requests.get(self.repo_latest_release_url)
            redirected_url = res.url
            version = redirected_url.split('/')[-1]
            return version
        except:
            return "Error fetching version"

    def launch_game(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        client_main = os.path.join(base_dir, "..", "client", "main.py")
        client_main = os.path.abspath(client_main)
        subprocess.Popen([sys.executable, client_main])
  