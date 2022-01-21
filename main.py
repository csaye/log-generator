import json, requests, sys
from datetime import datetime

# read config
try:
    config_file = open('./config.json', 'r')
    config_json = config_file.read()
    config = json.loads(config_json)
    config_file.close()
except FileNotFoundError:
    print('config.json not found')
    sys.exit()
except json.decoder.JSONDecodeError:
    print('invalid config.json')
    sys.exit()

# fetch github actions
try:
    url = f'https://api.github.com/users/{config["username"]}/events'
    response = requests.get(url)
    actions = response.json()
except ConnectionRefusedError:
    print('github connection refused')
    sys.exit()

# get log name with current date
now = datetime.now()
filename = f'{now.strftime("%Y-%m-%d")}.log.md'

# create log file
file = open(f'./logs/{filename}', 'w')
header = f'# {now.strftime("%A, %B %d, %Y %I:%M %p")}\n\n'
file.write(header)

# write log file
for action in actions:
    type = action['type']
    if type == 'PushEvent':
        payload = action['payload']
        commits = payload['commits']
        for commit in commits:
            message = commit['message']
            message = message.strip('.')
            file.write(f'- [X] {message}\n')

# close log file
file.close()
