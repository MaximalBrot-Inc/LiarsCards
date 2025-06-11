import requests

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
