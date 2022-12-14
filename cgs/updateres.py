# updating
from pprint import pprint
import requests
import configfile as configfile 
from bs4 import BeautifulSoup
import argparse, datetime



def login_update(username, password, uid, scheduleId, resourceId, day, starthour, endhour, referenceNumber, verbose=False):
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

        # after getting the token, let's get the reservationId by viewing the reservation the ref number page response
        view_ref_num = session.get(url=f'https://scop-sas.csfoy.ca/booked_sas/Web/reservation.php?rn={referenceNumber}')
        # pprint(view_ref_num.text)

        find_resid_soup = BeautifulSoup(view_ref_num.text, features='html.parser')
        reservationId = find_resid_soup.find('input', {'name':'reservationId'}).get('value')
        if verbose:
            print(f"reservationId: {reservationId}")

        posturl = "https://scop-sas.csfoy.ca/booked_sas/Web/ajax/reservation_update.php"
        payload = {
        'userId': uid,
        'scheduleId': scheduleId, # the sport id
        'resourceId': resourceId,
        'beginDate': day,
        'beginPeriod': starthour,
        'endDate': day,
        'endPeriod': endhour,
        'reservationTitle': '',
        'reservationDescription': '', 
        'reservationId': reservationId,
        'referenceNumber': referenceNumber,
        'reservationAction': 'update',
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
        except:
            error_msg = post_soup.find('div', id='failed-message').get_text()
            error_reason = post_soup.find('div', class_='error').get_text()
            print("\033[91m" + str(error_msg) + "\n" + "\033[93m" + str(error_reason)+"\033[0m")
        

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Update reservations at csfoy gym.")
    parser.add_argument("-rn", "--reference_number", type=str, help="Reservation reference number")
    parser.add_argument("-d", "--day", type=str, default=f"{datetime.date.today()}", help=f"day of reservation, format: {datetime.date.today()}")
    parser.add_argument("-u", "--userID", type=str, default=configfile.userID, help="userID used for reservation")
    parser.add_argument("-t", "--time", type=str, default=datetime.datetime.now().strftime("%H"), help="starting hour of the reservation")
    parser.add_argument("-r", "--resource", type=str, default="5", help="resource number (1-80)")
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
        f"\033[0;36mSending reservation update request for {starthour}, {args.day}\nAt resource {args.resource}, using {args.userID}, for scheduleId {args.scheduleId}.\033[0m"
        )
    login_update(configfile.username, configfile.password, uid=args.userID, scheduleId=args.scheduleId, resourceId=args.resource, day=args.day, starthour=starthour, endhour=endhour, referenceNumber=args.reference_number, verbose=args.verbose)