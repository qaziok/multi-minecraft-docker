import os

config = {}
with open('config.yml', 'r') as file:
    for line in file:
        name, value = line.rstrip().split(':',1)
        config[name] = value
        

VALUES = {
    "MAX_PLAYERS": "maxPlayers",
    "VERSION": "version",
    "WEBPORT": "webPort",
    "MOTD": "serverName",
    "WAKE_UP": "loginMessage"
}

for env, yml in VALUES.items():
    if v := os.getenv(env, None):
        config[yml] = f' {v}'

# Save the modified YAML file
with open('sleepingSettings.yml', 'w') as file:
    for i, (name, value) in enumerate(config.items()):
        print(f'{name}:{value}', file=file)