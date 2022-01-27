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

# check for arguments
if len(sys.argv) < 3:
    print('date and repo arguments must be given')
    sys.exit()

# get date
log_date = sys.argv[1]
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

# get repo
repo = sys.argv[2]

# fetch github events
try:
    url = f'https://api.github.com/repos/{config["username"]}/{repo}/events'
    response = requests.get(url)
    actions = response.json()
except requests.exceptions.ConnectionError:
    print('github connection refused')
    sys.exit()

# return if invalid repository
if type(actions) != list:
    print('invalid repo')
    sys.exit()
