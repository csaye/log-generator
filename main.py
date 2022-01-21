from datetime import date

# get log name with current date
today = date.today()
filename = f'{today.strftime("%Y-%m-%d")}.log.md'
