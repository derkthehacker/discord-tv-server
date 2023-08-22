import re

time1 = "PT2H9S"
time2 = "PT2H8M7S"
time3 = "PT8M9S"
time4 = 'PT45M9S'

def getSeconds(time):
    total_time = 0
    hour = re.search('([0-9])+H', time)
    if hour != None:
        hour = hour.group(0)
        hour = hour[:-1]
        total_time += int(hour) * 60 * 60
    minute = re.search('([0-9])+M', time)
    if minute != None:
        minute = minute.group(0)
        minute = minute[:-1]
        total_time += int(minute) * 60
    second = re.search('([0-9])+S', time)
    if second != None:
        second = second.group(0)
        second = second[:-1]
        total_time += int(second)
    print(total_time * 1000)
getSeconds(time1)
getSeconds(time2)
getSeconds(time3)
getSeconds(time4)