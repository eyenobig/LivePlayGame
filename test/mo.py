# import time, sys

# from danmu import DanMuClient

# def pp(msg):
#     print(msg.encode(sys.stdin.encoding, 'ignore').
#         decode(sys.stdin.encoding))
# dmc = DanMuClient('https://www.douyu.com/606118')
# if not dmc.isValid(): print('Url not valid')

# @dmc.danmu
# def danmu_fn(msg):
#         pp('[%s] %s' % (msg['NickName'], msg['Content']))

# @dmc.gift
# def gift_fn(msg):
#         pp('[%s] sent a gift!' % msg['NickName'])

# @dmc.other
# def other_fn(msg):
#         pp('Other message received')

# dmc.start(blockThread = True)
# import win32com.client, win32api, win32con
# from key import VK_CODE
# def press(*args):
#     for i in args:
#         win32api.keybd_event(VK_CODE[i], 0, 0, 0)
#         win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
# press('select')