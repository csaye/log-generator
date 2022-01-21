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
