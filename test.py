# from mo import asd


match = {'x':9,'y':1,'z':1}
# match = ['x','y','z']
def Model_Recod(data):
    Sum = 0
    for v in data:
        Sum += data[v]
    print(data["x"]/Sum)
    if data["x"]/Sum:
        pass
    # if data[v]/sum :
    #     pass
    return Sum
    # data['free']
Model_Recod(match)
# def Stat(data):
# 	obj = "{"
# 	for v in data:
# 		obj += '"' + v + '":0,'
# 	obj = eval(obj[:-1] + '}')
# 	return obj



# def AddLog(v,Log):

# 	Log[v] += 1

# 	# Log[x] += 1


# Log = Stat(match)

# AddLog("x",Log)
# AddLog("x",Log)
# AddLog("z",Log)
# AddLog("z",Log)
# AddLog("z",Log)
# AddLog("z",Log)
# AddLog("z",Log)

# AddLog("y",Log)
# AddLog("y",Log)
# AddLog("y",Log)
# AddLog("z",Log)
# AddLog("z",Log)
# AddLog("z",Log)
# AddLog("z",Log)

# print (Log)
# print (max(Log))








