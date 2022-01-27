import json, requests, sys

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

# get repo
repo = sys.argv[2]
