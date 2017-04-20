import os
import configparser
import time, sys
import win32com.client, win32api, win32con
from key import VK_CODE
from threading import Thread
from danmu import DanMuClient
#  生成 配置文件 如果有就退出

settings = []
shell = win32com.client.Dispatch("WScript.Shell")
match = ['x','y','z']
retime = time.time()
# 选择游戏
GAME = os.listdir('game')[0]

def Stat(data):
    obj = "{"
    for v in data:
        obj += '"' + v + '":"0",' 
    obj = eval(obj[:-1] + '}')
def remsg(msg):
    return msg.encode(sys.stdin.encoding, 'ignore').decode(sys.stdin.encoding)
def startemulator():
    if os.path.splitext(os.listdir('game')[0])[1] != ".sgm"or".ini":
        os.system('"%s\game\%s"' % (os.getcwd(), GAME))
def press(*args):
    '''
    press, release
    eg press('x', 'y', 'z')
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        if QUICK_PRESS == False:
            time.sleep(0.2)
        if QUICK_PRESS == True:
            time.sleep(.01)
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

while True:
    if os.path.isfile("settings.txt"):
        config = configparser.ConfigParser()
        config.read("settings.txt")

        URL = config.get('Settings', 'LIVEROOM').lower()
        APP = config.get('Settings', 'APP')
        QUICK_PRESS = config.getboolean('Settings', 'QUICK_PRESS')
        # CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()
        command_length = config.getint('Settings', 'LENGTH')

        break
    else:
        print("Let's make you a config file")
        settings.append("; Settings for Twitch Plays Pokemon bot")
        settings.append("[Settings]\n")


        settings.append("; Your LiveRoom ")
        print("Your LiveRoom")
        settings_url = input("完整链接: ")
        settings.append("LIVEROOM = " + settings_url + "\n")

        settings.append("; Name of the application you run the file from, I suggest VBA")
        print("Name of the application you run the file from, if Visual Boy Advance use VisualBoyAdvance")
        settings_app = input("Application name: ")
        settings.append("APP = " + settings_app + "\n")

        settings.append("; The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        print("The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        settings_length = input("Length: ")
        settings.append("LENGTH = " + settings_length + "\n")

        settings.append("; 是否直接转向")
        print("是否直接转向")
        settings_press = input("QUICK PRESS: ")
        settings.append("QUICK_PRESS = " + settings_press + "\n")

        with open("settings.txt", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')

while True:
    print("选择模式:  Democracy(民主),Anarchy(自由)")
    mode = input("Game type: ")
    if mode.lower() == "anarchy":
        break
    if mode.lower() == "democracy":
        print("设置 X 秒 读取命令行: ")
        democracy_time = float(input("(must be integer) X="))
        break

# Anarchy Game Mode
if mode.lower() == "anarchy":

    print("Starting %s" % GAME)
    time.sleep(1)

    emulator_job = Thread(target = startemulator, args = ())
    emulator_job.start()

    dmc = DanMuClient(URL)
    if not dmc.isValid(): print('Url not valid')

    @dmc.danmu
    def danmu_fn(msg):
        button = msg['Content'].lower()
        print(button)    
        if button in match:
            shell.AppActivate("VisualBoyAdvance")
            time.sleep(.02)
            press(button)
            record = time.strftime("%Y%m%d_%H", time.localtime())
            with open("record/"+record+".json", "a") as f:
                f.write(button + '\n')

    dmc.start(blockThread = True)
    


# Democracy Game Mode
if mode.lower() == "democracy":


    print("Starting %s" % GAME)
    time.sleep(1)
    emulator_job = Thread(target = startemulator, args = ())
    emulator_job.start()
    Log = Stat(match)
    dmc = DanMuClient(URL)
    if not dmc.isValid(): print('Url not valid')

    retime = time.time()


    @dmc.danmu
    def danmu_fn(msg):
        button = msg['Content'].lower()
        print("弹幕时间"+ str(time.time()))
        nowtime = time.time()
        # print(retime)
        if nowtime > retime + 20:
            retime = nowtime
        if button in match:
            shell.AppActivate("VisualBoyAdvance")
            time.sleep(.02)
            Log['x'] += 1
            
            press(button)
            record = time.strftime("%Y%m%d_%H", time.localtime())
            with open("record/"+record+".json", "a") as f:
                f.write(button + '\n')

    dmc.start(blockThread = True)
    
