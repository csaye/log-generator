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
