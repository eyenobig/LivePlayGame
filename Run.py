import os
import configparser
import time, sys,json,requests
import win32com.client, win32api, win32con
from key import Use_CODE
from threading import Thread
from danmu import DanMuClient
from key.object import DanmuRecord,VoteRecord

#  生成 配置文件 如果有就退出

settings = []
shell = win32com.client.Dispatch("WScript.Shell")
# 选择游戏
def Stat(data):
    obj = "{"
    for v in data:
        obj += '"' + v + '":0,'
    obj = eval(obj[:-1] + '}')
    return obj
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
    if args == "freedom" or args == "democracy":
        pass
    for i in args:
        win32api.keybd_event(Use_CODE[i], 0, 0, 0)
        if QUICK_PRESS == False:
            time.sleep(0.2)
        if QUICK_PRESS == True:
            time.sleep(.01)
        win32api.keybd_event(Use_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
def Maxconut(data):
    max = 0
    key = ''
    for k in data:
        if data[k] >= max:
            max = data[k]
            key = k
    return key
def Model_Recod(data):
    Sum = 0
    for v in data:
        Sum += data[v]
    if data['freedom']:
        if data['freedom']/Sum >= 0.6:
            return 'freedom'
    if data['democracy']:
        if data['democracy']/Sum >= 0.5:
            return 'democracy'
    else:
        return 0

def Time_load(Model):
    while True:
        global retime
        global Log

        if time.time() > retime + democracy_time:
            retime = time.time()
            # print(Log)
            # print(Time_re.__dict__)
            NewModel = Model_Recod(Log)
            if NewModel:
                DataJ = VoteRecord(NewModel,Log).json()
                requests.post("http://127.0.0.1:5000/vote", data=DataJ)
                ChangeModel(NewModel,Model)
            # print(Log)
            Fbutton = Maxconut(Log)
            Log = Stat(MATCH)
            shell.AppActivate("VisualBoyAdvance")
            time.sleep(.02)
            press(Fbutton)
            DataJ = VoteRecord(Fbutton,Log).json()
            VoteId = requests.post("http://127.0.0.1:5000/vote", data=DataJ)
            # print("投票结果" + Fbutton)
            DataJ = DanmuRecord(Model,Fbutton,VoteId.text).json()
            requests.post("http://127.0.0.1:5000/record", data=DataJ)
def Time_Change(Model):

    while True:
        global retime
        global Log
        if time.time() > retime + democracy_time:
            retime = time.time()
            NewModel = Model_Recod(Log)
            Log = Stat(MATCH)
            if NewModel:
                DataJ = VoteRecord(NewModel,Log).json()
                requests.post("http://127.0.0.1:5000/vote", data=DataJ)
                ChangeModel(NewModel,Model)
def PlayGame(Model):
    global Time_re
    global retime
    global Log
    global dmc
    dmc = DanMuClient(URL)
    if not dmc.isValid(): print('Url not valid')
    Model = Model.lower()
    retime = time.time()
    Log = Stat(MATCH)
    if Model == 'freedom' :
        Time_re = Thread(target = Time_Change, args = (Model,))
        Time_re.start()
    if Model == 'democracy' :
        Time_re = Thread(target = Time_load, args = (Model,))
        Time_re.start()
    @dmc.danmu
    def danmu_fn(msg):
        button = msg['Content'].lower()

        print(msg)
        if button in MATCH:
            Log[button] += 1
            if Model == 'freedom':
                shell.AppActivate("VisualBoyAdvance")
                time.sleep(.02)
                press(button)
                DataJ = DanmuRecord(msg['NickName'],button).json()
                requests.post("http://127.0.0.1:5000/record", data=DataJ)
            if Model == 'democracy':
                Log[button] += 1

    dmc.start(blockThread = True)

def ChangeModel(Model,NowModel):
    if Model == NowModel:
        print("与现在模式相同")
    if Model != NowModel:
        print("切换模式中")
        dmc.stop()
        Time_re._is_stopped = True
        PlayGame(Model)

while True:
    if os.path.isfile("settings.txt"):
        config = configparser.ConfigParser()
        config.read("settings.txt")

        URL = config.get('Settings', 'LIVEROOM').lower()
        APP = config.get('Settings', 'APP')
        QUICK_PRESS = config.getboolean('Settings', 'QUICK_PRESS')

        MATCH = config.get('Settings', 'MATCH_PRESS').split(",")
        GAME = config.get('Settings', 'GAME')

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

        settings.append("; 是否直接转向")
        print("是否开启直接转向")
        settings_press = input("QUICK PRESS: ")
        settings.append("QUICK_PRESS = " + settings_press + "\n")

        settings.append("; 设置录入按键")
        print("设置录入按键")
        settings_press = input("MATCH PRESS: ")
        settings.append("MATCH_PRESS = 'freedom','democracy'," + settings_press + "\n")

        settings.append("; 设置游戏[Game]文件夹下")
        print("设置游戏[Game]文件夹下")
        settings_press = input("Game: ")
        settings.append("GAME = " + settings_press + "\n")

        with open("settings.txt", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')

# while True:
#     # print("选择模式:  Democracy(民主),freedom(自由)")
#     # mode = input("Game type: ")
#     # if mode.lower() == "freedom":
#     #     break
#     # if mode.lower() == "democracy":
#     print("设置 X 秒 读取命令行: ")
#     democracy_time = float(input("(must be integer) X="))
#     break
democracy_time = 3


print("Starting %s" % GAME)
time.sleep(1)

emulator_job = Thread(target = startemulator, args = ())
emulator_job.start()




# PlayGame(mode)
# PlayGame("Democracy")
