# CGS API 
[![Downloads](https://pepy.tech/badge/cgs)](https://pepy.tech/project/cgs) [![PyPI](https://img.shields.io/pypi/v/cgs?color=%230eb00e)](https://pypi.org/project/cgs)
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
In order to get started you will need to first set matricule & password and run `--get-uid` to fetch uid (make sure that your matricule & password are correct else you will not be able to get your uid). 
```bash
cgs config --mat your_matricule
cgs config --pwd your_password
cgs config --get-uid
```
verify credentials with: `cgs config --show`

list options with: `cgs --help`

### ex: create reservation at 2023-01-12 at 12:00 (time is 0-24)
```bash
cgs create -d 2023-01-12 -t 12
```
list possible flags with: `cgs create --help`

## Contributing

Feel free to contribute!  DM me on twitter [@msa720360](https://twitter.com/msa720360) if you have any questions.
