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
match = ["anarchy","democracy",'x','y','z']
# 选择游戏
GAME = os.listdir('game')[0]
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
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        if QUICK_PRESS == False:
            time.sleep(0.2)
        if QUICK_PRESS == True:
            time.sleep(.01)
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
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
    if data['anarchy']:
        if data['anarchy']/Sum >= 0.6:
            return 'anarchy'
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
            # print("到点了")
            print(Log)
            # print(Time_re.__dict__)
            NewModel = Model_Recod(Log)
            if NewModel:
                ChangeModel(NewModel,Model)
            Fbutton = Maxconut(Log)
            Log = Stat(match)
            shell.AppActivate("VisualBoyAdvance")
            time.sleep(.02)
            press(Fbutton)
            print("投票结果" + Fbutton)
            record = time.strftime("%Y%m%d_%H", time.localtime())
            with open("record/"+record+".json", "a") as f:
                f.write(Fbutton + '\n')
def Time_Change(Model):

    while True:
        global retime
        global Log
        if time.time() > retime + democracy_time:
            retime = time.time()
            NewModel = Model_Recod(Log)
            Log = Stat(match)
            if NewModel:
                ChangeModel(NewModel,Model)
def PlayGame(Model):
    global Time_re
    global retime
    global Log
    dmc = DanMuClient(URL)
    if not dmc.isValid(): print('Url not valid')
    Model = Model.lower()
    retime = time.time()
    Log = Stat(match)
    if Time_Model == False and Model == 'anarchy' :
        Time_re = Thread(target = Time_Change, args = (Model,))
        Time_re.start()
    if Time_Model == False and Model == 'democracy' :
        Time_re = Thread(target = Time_load, args = (Model,))
        Time_re.start()
    @dmc.danmu
    def danmu_fn(msg):
        button = msg['Content'].lower()
        print(button)
        if button in match:
            Log[button] += 1
            if Model == 'anarchy':
                shell.AppActivate("VisualBoyAdvance")
                time.sleep(.02)
                press(button)
                record = time.strftime("%Y%m%d_%H", time.localtime())
                with open("record/"+record+".json", "a") as f:
                    f.write(button + '\n')
            if Model == 'democracy':
                Log[button] += 1
    dmc.start(blockThread = True)

def ChangeModel(Model,NowModel):
    if Model == NowModel:
        print("与现在模式相同")
    if Model != NowModel:
        print("切换模式中")
        dmc.stop()
        if Time_Model == False:
            Time_re._is_stopped = True
        PlayGame(Model)

while True:
    if os.path.isfile("settings.txt"):
        config = configparser.ConfigParser()
        config.read("settings.txt")

        URL = config.get('Settings', 'LIVEROOM').lower()
        APP = config.get('Settings', 'APP')
        QUICK_PRESS = config.getboolean('Settings', 'QUICK_PRESS')
        Time_Model = config.getboolean('Settings', 'Time_Model')
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

        settings.append("; 1是弹幕记录时间 0是时间记录时间")
        print("时间记录方式")
        print("1是弹幕记录时间 0是时间记录时间")
        settings_Time_Model = input("Time Model: ")
        settings.append("Time_Model = " + settings_Time_Model + "\n")

        with open("settings.txt", "w") as f:
            for each_setting in settings:
                f.write(each_setting + '\n')

while True:
    # print("选择模式:  Democracy(民主),Anarchy(自由)")
    # mode = input("Game type: ")
    # if mode.lower() == "anarchy":
    #     break
    # if mode.lower() == "democracy":
    print("设置 X 秒 读取命令行: ")
    democracy_time = float(input("(must be integer) X="))
    break


print("Starting %s" % GAME)
time.sleep(1)

emulator_job = Thread(target = startemulator, args = ())
emulator_job.start()




# PlayGame(mode)
PlayGame("Anarchy")
