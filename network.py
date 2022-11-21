import socket
import socks
import requests

def is_proxy_working() -> bool:
    """returns true if the proxy is working"""
    virgin_ip = requests.get('http://jsonip.com').json()['ip'] #needs to be defined before activating socket
    ip='localhost' # change your proxy's ip
    port = 9050 # change your proxy's port
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
    socket.socket = socks.socksocket
    try:
        response = requests.get('http://jsonip.com')
        received_ip = response.json()['ip']
        print(received_ip)
        if received_ip == virgin_ip:
            return False
        else:
            return True
    except:
        print("proxy not working so stopped")
        return False






  

