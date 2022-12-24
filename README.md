# CGS API
### Command line tool in python to place & update reservations at Cégep Sainte-Foy gym.

## Installing
```bash
$ git clone "https://github.com/Msa360/cgs-csfoy-gym.git"
$ cd API_salle
$ pip3 install -r requirements.txt 
```
### you will need to set username & password
```bash
cgs --set-matricule your_matricule
cgs --set-password your_password
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

## Usage
```python
import cgs
# login and create a reservation
cgs.login_create()
```
### command line usage
```bash
python3 -m /your/path/cgs -h
```
