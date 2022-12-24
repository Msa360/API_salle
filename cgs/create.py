# creating 
from pprint import pprint
import requests
from .utils import configfile
from bs4 import BeautifulSoup
import argparse, datetime



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

        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Create reservations at csfoy gym.")
    parser.add_argument("-d", "--day", type=str, default=f"{datetime.date.today()}", help=f"day of reservation, format: {datetime.date.today()}")
    parser.add_argument("-u", "--userID", type=str, default=configfile.userID, help="userID used for reservation")
    parser.add_argument("-t", "--time", type=str, default=datetime.datetime.now().strftime("%H"), help="starting hour of the reservation")
    parser.add_argument("-r", "--resource", type=str, default="30", help="resource number (1-80)")
    parser.add_argument("-s", "--scheduleId", type=str, default=configfile.gym_scheduleId, help="sport id (default is 64 for gym)")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="prints the html response")

    args = parser.parse_args()
    
    # adds zero to single digits
    if len(args.time) < 2:
        starthour = "0" + args.time + ":00:00"
    else:
        starthour = args.time + ":00:00"

    endhour = str(int(args.time) + 1)
    if len(endhour) < 2:
        endhour = "0" + endhour + ":00:00"
    else:
        endhour = endhour + ":00:00"

    # correcting resource id
    OG_resource_number = int(args.resource)
    resource_number = OG_resource_number
    if OG_resource_number > 25:
        resource_number += 208
    if OG_resource_number > 60:
        resource_number += 144
    resource_number = str(resource_number + 4745)
    print(
        f"\033[0;36mSending reservation request for {starthour}, {args.day}\nAt resource {args.resource}, using {args.userID}, for scheduleId {args.scheduleId}.\033[0m"
        )
    login_create(configfile.username, configfile.password, uid=args.userID, scheduleId=args.scheduleId, resourceId=resource_number, day=args.day, starthour=starthour, endhour=endhour, verbose=args.verbose)
