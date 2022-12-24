
import requests
from bs4 import BeautifulSoup
import json, os

# from . import configfile

def find_ressource_id(sportrange) -> list:
    '''finds the ressource id of an element'''
    login_data = {
        'email': configfile.username,
        'password': configfile.password,
        'login': 'submit',
        'resume': ''
    }
    try:
        with requests.session() as session:
            login_response = session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=configfile.proxies)
            r = session.get(f'https://scop-sas.csfoy.ca/booked_sas/Web/schedule.php?sid={sportrange}', proxies=configfile.proxies)
            ress_soup = BeautifulSoup(r.text, features='html.parser')
            ress_id_list = []
            for i in ress_soup.find_all('a', {'class': 'resourceNameSelector'}):
                ress_id_list.append(i.get('resourceid'))

            return ress_id_list
    except:
        return []
        
def find_reference_num(resourceId):
    
    pass

class _Config():
    """
    Parses and create a config object from configfile.json
    """
    def __init__(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'configfile.json'), "r") as f:
            self.json = json.load(f)
        self.gym_scheduleId = self.json["gym_scheduleId"]
        self.userID = self.json["userID"]
        self.username = self.json["username"]
        self.password = self.json["password"]
        self.proxies = self.json["proxies"]

    def __str__(self) -> str:
        return self.json.__str__()

    def mod(self, key:str, value):
        """
        modify the value for the specified key in the configfile.json
        "userID", "username", "password", "proxies"
        """
        self.json[key] = value
        with open(os.path.join(os.path.dirname(__file__), 'configfile.json'), "w") as f:
            json.dump(self.json, f)
        
configfile = _Config()
# print(find_ressource_id(53))