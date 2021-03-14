# analyze maslog.txt
# date and time log
# times of times/day
# total times per (overall, month, weekday)
# avg time/day per (overall, month, weekday)
# how many per hour (overall, month, weekday)


with open('/home/pi/discordbot/maslog.txt', 'r') as f:
    lines = f.readlines()
nlines =[]
for line in lines:
    nlines.append(line[:-1].split(" ", 1))
print(nlines)