import json, requests, sys
from datetime import date, datetime, timedelta, timezone

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

# get date
log_date = sys.argv[1] if len(sys.argv) > 1 else 'today'
if log_date == 'today': log_date = date.today()
elif log_date == 'yesterday': log_date = date.today() - timedelta(days=1)
else:
    try:
        log_date = datetime.strptime(log_date, '%Y-%m-%d').date()
    except ValueError:
        print('invalid date given (YYYY-MM-DD)')
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
filename = f'{log_date.strftime("%Y-%m-%d")}.log.md'

# create log file
file = open(f'./logs/{filename}', 'w')
header = f'# {log_date.strftime("%A, %B %d, %Y %I:%M %p")}\n\n'
file.write(header)

# write log file
for action in actions:
    type = action['type']
    if type == 'PushEvent':
        # get creation date
        created = action['created_at']
        created = created.replace('T', ' ').replace('Z', '')
        created = datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
        created = created.replace(tzinfo=timezone.utc).astimezone(tz=None)
        if log_date != created.date(): continue
        # get repo name
        repo = action['repo']
        repo_name = repo['name']
        repo_name = repo_name.split('/')[1]
        # get commits
        payload = action['payload']
        commits = payload['commits']
        for commit in commits:
            message = commit['message']
            message = message.strip('.')
            file.write(f'- [X] {message}\n')

# close log file
file.close()
