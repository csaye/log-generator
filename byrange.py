import json, requests, sys
from datetime import date, datetime, timedelta, timezone
from random import shuffle, choice
from os import system

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

# get start and end dates
start_date = config['start_date']
end_date = config['end_date']

# verify start date
try:
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
except ValueError:
    print('invalid start date given (YYYY-MM-DD)')
    sys.exit()

# verify end date
try:
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
except ValueError:
    print('invalid end date given (YYYY-MM-DD)')
    sys.exit()

log_date = start_date

# run for maximum iterations
for i in range(config['max_iterations']):

    # get repo
    repo = choice(config['repos'])

    # get times
    day_name = log_date.strftime('%A')
    times = config['times'][day_name]

    # fetch github events
    try:
        url = f'https://api.github.com/repos/{repo}/events'
        response = requests.get(url)
        actions = response.json()
    # handle connection error
    except requests.exceptions.ConnectionError:
        print('github connection refused')
        sys.exit()

    # return if invalid repository
    if type(actions) != list:
        print('invalid repo')
        sys.exit()

    # get commit messages
    messages = []
    for action in actions:
        action_type = action['type']
        if action_type == 'PushEvent':
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

    # rename repo and get commit ending
    repo = '/'.join(repo.split('/')[1:])
    ending = f'{log_date.strftime("%b %-d")} ({times[2]})'

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
    file.write(f'\n{on_phrase} {repo}.\n')

    # close file
    file.close()

    # make commit
    system(f'git add logs/{filename}')
    system(f'git commit -m "docs: Add sign on for {ending}"')

    # open log file
    file = open(f'./logs/{filename}', 'a')

    # close log
    file.write(f'\n{header} {times[1]}\n')
    for message in messages:
        file.write(f'- [X] {message}\n')

    # write off phrase
    off_phrases = config['off_phrases']
    off_phrase = choice(off_phrases)
    file.write(f'\n{off_phrase} {repo}.\n')
    # update date
    if log_date == end_date: break
    log_date += timedelta(days=1)
