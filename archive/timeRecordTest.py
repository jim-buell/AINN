import time

#record time of headline fetch in milliseconds from epoch
currentTime = round(time.time() * 1000)
f = open("elapsedTime.txt", "w")
timeStr = str(currentTime)
f.write(timeStr)
f.close()
print(timeStr)