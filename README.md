# CGS API
### Command line tool in python to place & update reservations at Cégep Sainte-Foy gym.

## Installing
```bash
pip install cgs
```

## Usage
```python
import cgs

# login and create a reservation
cgs.login_create()
```
## Command line usage
you will need to first set username & password (put a number between 11500-12500 if you don't know your uid or dm me on twitter to get it)
```bash
cgs --set-uid your_uid
cgs --set-matricule your_matricule
cgs --set-password your_password
```
### verify credentials with: `cgs config`
### list options with: `cgs --help`
### create reservation at 13 (time is 24-clock)
```bash
cgs create -t 13
```
### list possible flags with: `cgs create --help`

## Contributing

Feel free to contribute! Right now the next step is to make a function that automatically fetches the userID, since most people don't know it. It is possible to fetch it only with matricule & password.
