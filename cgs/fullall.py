# full all reserve of all stuff
import random

from . import configfile
from .create import login_create
from .utils import find_ressource_id




# hours_list = ['08:00:00','09:00:00','10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00']
# days_list = ['2022-03-17', '2022-03-18']
# ressources_id = ['4251', '4252', '4253', '4254', '4255', '4256', '4257']

def reserve_all(sport_id_range: list, days_list: list) -> None:
    """
    Reserves all specified fields.
    """
    tries = 0
    successful_tries = 0
    hours_list = ['10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00']
    ressources_id = find_ressource_id(sport_id_range[0]) #['4251', '4252', '4253', '4254', '4255', '4256', '4257']
    
    for sport in sport_id_range:
        for day in days_list:
            for hour in hours_list:
                if hours_list.index(hour) != len(hours_list) - 1:
                    end_hour =  hours_list[hours_list.index(hour) + 1]
                    for ressid in ressources_id: 
                        uid = str(random.randint(12000, 12100))
                        try:
                            login_create(username=configfile.username, password=configfile.password, uid=uid, scheduleId=str(sport), resourceId=ressid, day=day, starthour=hour, endhour=end_hour)
                            successful_tries += 1
                            tries += 1
                            print(f'request worked with uid={uid}, ressid={ressid}, day={day}, hour={hour}, endhour={end_hour}')
                        except:
                            tries += 1
                            print('request failed')

    print(f"{successful_tries} successful tries on {tries} tries.")


# print(requests.get('http://jsonip.com').json()['ip'])
# reserve_all([53], ['2022-04-30'])
    
