import requests
from bs4 import BeautifulSoup
import json, os, platform, tempfile

def find_ressource_id(username, password, sportrange, proxies=None) -> list:
    '''finds the ressource id of an element'''
    login_data = {
        'email': username,
        'password': password,
        'login': 'submit',
        'resume': ''
    }
    try:
        with requests.session() as session:
            login_response = session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=proxies)
            r = session.get(f'https://scop-sas.csfoy.ca/booked_sas/Web/schedule.php?sid={sportrange}', proxies=proxies)
            ress_soup = BeautifulSoup(r.text, features='html.parser')
            ress_id_list = []
            for i in ress_soup.find_all('a', {'class': 'resourceNameSelector'}):
                ress_id_list.append(i.get('resourceid'))

            return ress_id_list
    except:
        return []



class _Config():
    """
    Parses and create a config object from configcgs.json
    """
    def __init__(self) -> None:
        # for production - from https://github.com/instaloader/instaloader/blob/3cc29a4ceb3ff4cd04a73dd4b20979b03128f454/instaloader/instaloader.py#L30
        try: # if file exist
            with open(os.path.join(self._get_config_dir(),'configcgs.json'), "r") as f:
                self.json = json.load(f)
        except:
            try: # if file not exist
                self.json = {
                    "gym_scheduleId": "64", 
                    "userID": "", 
                    "username": "", 
                    "password": "", 
                    "proxies": {}
                }
                with open(os.path.join(self._get_config_dir(),'configcgs.json'), "w+") as f:
                    json.dump(self.json, f)
            except:
                raise Exception("If you are having problems or you are using Windows, CGS will soon be available, see: https://github.com/Msa360/cgs-csfoy-gym for more info, or reach out to the devs.")
        self.gym_scheduleId = self.json["gym_scheduleId"]
        self.userID = self.json["userID"]
        self.username = self.json["username"]
        self.password = self.json["password"]
        self.proxies = self.json["proxies"]

    def __str__(self) -> str:
        return self.json.__str__()

    # https://github.com/instaloader/instaloader/blob/3cc29a4ceb3ff4cd04a73dd4b20979b03128f454/instaloader/instaloader.py#L30
    def _get_config_dir(self) -> str:
        if platform.system() == "Windows":
            # on Windows, use %LOCALAPPDATA%\
            localappdata = os.getenv("LOCALAPPDATA")
            if localappdata is not None:
                return localappdata
            # legacy fallback - store in temp dir if %LOCALAPPDATA% is not set
            return os.path.join(tempfile.gettempdir(), ".cgs-python")
        # on Unix, use ~/.config/
        return os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

    def mod(self, key:str, value):
        """
        modify the value for the specified key in the configcgs.json
        "userID", "username", "password", "proxies"
        """
        self.json[key] = value
        # for production
        with open(os.path.join(self._get_config_dir(), 'configcgs.json'), "w") as f:
            json.dump(self.json, f)
        
configfile = _Config()