staticFiles = ["verbsTrans", "ideo"]

part = "verbsTrans"

if not any(x in staticFiles for x in part):
	for item in staticFiles:
		print(item)
else:
	print(" In")