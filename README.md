# API SALLE
Command line tool in python to use an API of a gym.

### Installing
```shell
$ git clone "https://github.com/Msa360/API_salle.git"
$ cd API_salle
$ pip3 install -r requirements.txt 
```
Create a file called "configfile.py" and modify your credentials:

```python
# configfile.py

gym_scheduleId = "64"  # sportID (64 for gym)
userID =  "11633"      # userID
username = 2512534     # matricule
password = "password"  # password

# if no proxy needed
proxies = {}  

# if using proxies
proxies = {
    # example proxies
    "https": "46.145.102.101:3428",
    "http": "46.145.102.101:3428"
}
```
