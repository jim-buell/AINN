import time

f = open(r"elapsedTime.txt", "r")
lastTime = int(f.read().rstrip())
currentTime = round(time.time() * 1000)
print("Time now is ", currentTime)
elapsedTime = (currentTime - lastTime)
print("Elapsed time is ", elapsedTime)
if elapsedTime >= 3600000:
	print("Need to get new")
	#fetchNew()