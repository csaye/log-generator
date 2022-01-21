import json, requests
from datetime import date

# read config
config_file = open('./config.json', 'r')
config_json = config_file.read()
config = json.loads(config_json)
config_file.close()

# fetch github actions
url = f'https://api.github.com/users/{config["username"]}/events'
response = requests.get(url)
actions = response.json()

# get log name with current date
today = date.today()
filename = f'{today.strftime("%Y-%m-%d")}.log.md'

# create log file
file = open(f'./logs/{filename}', 'w')
file.close()
