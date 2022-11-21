
from pprint import pprint
import requests
import configfile 
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description="update reservations")


def login_update(username, password, uid, resourceId, day, starthour, endhour, referenceNumber, verbose=False):
    login_data = {
        'email': username,
        'password': password,
        'login': 'submit',
        'resume': ''
    }
    with requests.session() as session:
        login_response = session.post('https://scop.cegep-ste-foy.qc.ca/booked/Web/index.php', data=login_data, proxies=configfile.proxies)
        

        login_soup = BeautifulSoup(login_response.text, features='html.parser')
        csrf = login_soup.find('input', id='csrf_token').get('value')
        if verbose:
            print(f"csrf: {csrf}")

        # after getting the token, let's get the reservationId by viewing the reservation the ref number page response
        view_ref_num = session.get(url=f'https://scop.cegep-ste-foy.qc.ca/booked/Web/reservation.php?rn={referenceNumber}')
        # pprint(view_ref_num.text)

        find_resid_soup = BeautifulSoup(view_ref_num.text, features='html.parser')
        reservationId = find_resid_soup.find('input', {'name':'reservationId'}).get('value')
        if verbose:
            print(f"reservationId: {reservationId}")

        posturl = "https://scop.cegep-ste-foy.qc.ca/booked/Web/ajax/reservation_update.php"
        payload = {
        # 'userId': '12493',
        'userId': uid,
        'scheduleId': '64', # the sport id
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
            print(success_msg.get_text())
        except:
            error_msg = post_soup.find('div', id='failed-message').get_text()
            error_reason = post_soup.find('div', class_='error').get_text()
            print(str(error_msg) + "\n" + str(error_reason))
        

    

if __name__ == "__main__":
    
    login_update(configfile.username, configfile.password, uid='18194', resourceId='4747', day='2022-11-09', starthour='11:00:00', endhour='12:00:00', referenceNumber='635e955aefbe8660119916', verbose=False)