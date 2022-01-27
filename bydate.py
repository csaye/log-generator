import json, requests, sys
from datetime import date, datetime, timedelta, timezone
from random import shuffle, choice

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

# get times
day_name = log_date.strftime('%A')
times = config['times'][day_name]

# fetch github actions
try:
    url = f'https://api.github.com/users/{config["username"]}/events'
    response = requests.get(url)
    actions = response.json()
except requests.exceptions.ConnectionError:
    print('github connection refused')
    sys.exit()

# get commit messages
messages = []
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
        repo = repo['name']
        repo = repo.split('/')[1]
        # get commits
        payload = action['payload']
        commits = payload['commits']
        for commit in commits:
            message = commit['message']
            message = message.strip('.')
            messages.append(message)

# choose messages
shuffle(messages)
message_count = config["message_count"]
messages = messages[:message_count]

# open log file
filename = f'{log_date.strftime("%Y-%m-%d")}.log.md'
file = open(f'./logs/{filename}', 'w')
header = f'# {log_date.strftime("%A, %B %d, %Y")}'

# open log
file.write(f'{header} {times[0]}\n')
for message in messages:
    file.write(f'- [ ] {message}\n')

# write on phrase
on_phrases = config['on_phrases']
on_phrase = choice(on_phrases)
file.write(f'\n{on_phrase} {repo}.\n\n')

# close log
file.write(f'{header} {times[1]}\n')
for message in messages:
    file.write(f'- [X] {message}\n')

# write off phrase
off_phrases = config['off_phrases']
off_phrase = choice(off_phrases)
file.write(f'\n{off_phrase} {repo}.\n')

# write close phrase
close_phrases = config['close_phrases']
close_phrase = choice(close_phrases)
message = choice(messages)
file.write(f'{close_phrase} {message.lower()}.\n')

# close log file
file.close()
