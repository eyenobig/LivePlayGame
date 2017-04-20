
# match = {'x':'1','y':'1','z':'1'}
match = ['x','y','z']

def Stat(data):
	obj = "{"
	for v in data:
		obj += '"' + v + '":0,' 
	obj = eval(obj[:-1] + '}')	
	return obj

	
def AddLog(v,Log):

	Log[v] += 1

	# Log[x] += 1


Log = Stat(match)

AddLog("x",Log)
AddLog("x",Log)
AddLog("x",Log)
AddLog("x",Log)
AddLog("x",Log)
AddLog("x",Log)
AddLog("x",Log)

AddLog("y",Log)
AddLog("y",Log)
AddLog("y",Log)
AddLog("y",Log)
AddLog("y",Log)
AddLog("y",Log)

print (Log)
print (max(Log))