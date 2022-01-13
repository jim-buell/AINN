import time


mainStr = "Hello World"

currentDisp = ""
for letter in mainStr:
	currentDisp = currentDisp + letter
	print(currentDisp)
	time.sleep(1)
