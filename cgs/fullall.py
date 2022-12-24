# full all reserve of all stuff
from pprint import pprint
import random
import requests
from bs4 import BeautifulSoup
from .utils import configfile
from .create import login_create
from .utils import find_ressource_id




# hours_list = ['08:00:00','09:00:00','10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00']
# days_list = ['2022-03-17', '2022-03-18']
# ressources_id = ['4251', '4252', '4253', '4254', '4255', '4256', '4257']
def login_create(username: str, password: str, uid: str, scheduleId: str, resourceId: str, day: str, starthour: str, endhour: str, verbose=False): #must all be strings
    '''login and create a reservation, all params must be strings'''
    login_data = {
        'email': username,
        'password': password,
        'login': 'submit',
        'resume': ''
    }
    with requests.session() as session:
        login_response = session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=configfile.proxies)
        

        login_soup = BeautifulSoup(login_response.text, features='html.parser')
        csrf = login_soup.find('input', id='csrf_token').get('value')
        if verbose:
            print(f"csrf: {csrf}")

        # after getting the token, let's reserve
        posturl = "https://scop-sas.csfoy.ca/booked_sas/Web/ajax/reservation_save.php"
        payload = {
        # 'userId': '12493',
        # 'scheduleId': '64',
        'userId': uid,
        'scheduleId': scheduleId, # the sport id
        'resourceId': resourceId,
        'beginDate': day,
        'beginPeriod': starthour,
        'endDate': day,
        'endPeriod': endhour,
        'reservationTitle': '',
        'reservationDescription': '',
        'reservationId': '',
        'referenceNumber': '',
        'reservationAction': 'create',
        'seriesUpdateScope': 'full',
        'CSRF_TOKEN': csrf
        }

        response = session.post(url=posturl, data=payload, proxies=configfile.proxies)
        if verbose:
            pprint(response.text)
        post_soup = BeautifulSoup(response.text, features='html.parser')
        try:
            success_msg = post_soup.find('div', id='created-message')
            print("\033[92m"+success_msg.get_text()+"\033[0m")
            ref_num = post_soup.find('div', id="reference-number").get_text().split()[-1]
            if verbose:
                print(f"reference number: {ref_num}")
            return ref_num
        except:
            error_msg = post_soup.find('div', id='failed-message').get_text()
            error_reason = post_soup.find('div', class_='error').get_text()
            print("\033[91m" + str(error_msg) + "\n" + "\033[93m" + str(error_reason)+"\033[0m")
            return None


def reserve_all(sport_id_range: list, days_list: list) -> None:
    """
    Reserves all specified fields.
    """
    tries = 0
    successful_tries = 0
    hours_list = ['10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00']
    ressources_id = find_ressource_id(sport_id_range[0]) #['4251', '4252', '4253', '4254', '4255', '4256', '4257']
    
    login_data = {
        'email': configfile.username,
        'password': configfile.password,
        'login': 'submit',
        'resume': ''
    }
    with requests.session() as session:
        login_response = session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=configfile.proxies)
        login_soup = BeautifulSoup(login_response.text, features='html.parser')
        csrf = login_soup.find('input', id='csrf_token').get('value')

        for sport in sport_id_range:
            for day in days_list:
                for hour in hours_list:
                    if hours_list.index(hour) != len(hours_list) - 1:
                        end_hour =  hours_list[hours_list.index(hour) + 1]
                        for ressid in ressources_id: 
                            uid = str(random.randint(12000, 12100))




                            # after getting the token, let's reserve
                            posturl = "https://scop-sas.csfoy.ca/booked_sas/Web/ajax/reservation_save.php"
                            payload = {
                            # 'userId': '12493',
                            # 'scheduleId': '64',
                            'userId': uid,
                            'scheduleId': str(sport), # the sport id
                            'resourceId': ressid,
                            'beginDate': day,
                            'beginPeriod': hour,
                            'endDate': day,
                            'endPeriod': end_hour,
                            'reservationTitle': '',
                            'reservationDescription': '',
                            'reservationId': '',
                            'referenceNumber': '',
                            'reservationAction': 'create',
                            'seriesUpdateScope': 'full',
                            'CSRF_TOKEN': csrf
                            }

                            response = session.post(url=posturl, data=payload, proxies=configfile.proxies)
                            # if verbose:
                                # pprint(response.text)
                            post_soup = BeautifulSoup(response.text, features='html.parser')
                            try:
                                success_msg = post_soup.find('div', id='created-message')
                                print("\033[92m"+success_msg.get_text()+"\033[0m")
                                ref_num = post_soup.find('div', id="reference-number").get_text().split()[-1]
                                # if verbose:
                                #     print(f"reference number: {ref_num}")
                            except:
                                try:
                                    error_msg = post_soup.find('div', id='failed-message').get_text()
                                    error_reason = post_soup.find('div', class_='error').get_text()
                                    print("\033[91m" + str(error_msg) + "\n" + "\033[93m" + str(error_reason)+"\033[0m")
                                    ref_num = None
                                except:
                                    pprint(response.text)
                                    raise Exception("nor success nor error message was found by bs4")


                            # ref_num = login_create(username=configfile.username, password=configfile.password, uid=uid, scheduleId=str(sport), resourceId=ressid, day=day, starthour=hour, endhour=end_hour)
                            if (ref_num != None):
                                successful_tries += 1
                                tries += 1
                                print(f'request worked with uid={uid}, ressid={ressid}, day={day}, hour={hour}, endhour={end_hour}')
                            else:
                                tries += 1
                                print('request failed')

    print(f"{successful_tries} successful tries on {tries} tries.")


# print(requests.get('http://jsonip.com').json()['ip'])
# reserve_all([53], ['2022-04-30'])
    
