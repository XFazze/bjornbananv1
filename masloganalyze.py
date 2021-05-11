# analyze maslog.txt
# date and time log
# times of times/day
# total times per (overall, month, weekday)
# avg time/day per (overall, month, weekday)
# how many per hour (overall, month, weekday)

x = 0
with open('/home/pi/discordbot/maslog.txt', 'r') as f:
    lines = f.readlines()
nlines =[]
for line in lines:
    x += 1
    print(line)
    nlines.append(line[:-1].split(" ", 1))
#print(nlines)
print(x)
