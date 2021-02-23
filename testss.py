import math
import time
start_time = time.time()
with open('/home/pi/discordbot/vc_logs.txt', 'r') as file:
    filelines = file.readlines()
minutes={}
for line in filelines:
    linelist = line.split(" ")
    if linelist[1] == "connect":
        line_num = filelines.index(line)
        for iline in filelines[line_num:]:
            ilinelist = iline.split(" ")
            if ilinelist[1] == "disconnect" and str(linelist[3])[:-1] == str(ilinelist[3])[:-1]:
                trime = int(math.floor((float(ilinelist[0])/60 - float(linelist[0])/60)))
                name = str(linelist[3])[:-1]
                #print(name, line_num, trime)
                if name in minutes.keys():
                    minutes[name] = minutes[name]+trime
                else:
                    minutes[name] = trime
                break

minutes =  dict(sorted(minutes.items(), key=lambda item: item[1]))
for item in minutes:
    print(minutes[item],"   :   ", item)
print("My program took", time.time() - start_time, "to run")