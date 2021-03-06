import json
with open('/home/pi/discordbot/management/tsbot.json', 'r+') as f:
    tsbot = json.load(f)
print(tsbot)