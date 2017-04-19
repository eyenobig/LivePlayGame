import os
import configparser
import time, sys
import win32com.client, win32api, win32con
from key import VK_CODE
from threading import Thread
from danmu import DanMuClient
#  生成 配置文件 如果有就退出

settings = []
test = ''
shell = win32com.client.Dispatch("WScript.Shell")

# 选择游戏
GAME = os.listdir('game')[0]

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').decode(sys.stdin.encoding))
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
        print("过段时间")
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
    with open("lastsaid.txt", "w") as f:
        f.write("")

    print("Starting %s" % GAME)
    time.sleep(1)
    emulator_job = Thread(target = startemulator, args = ())
    emulator_job.start()

    dmc = DanMuClient(URL)
    if not dmc.isValid(): print('Url not valid')

    # @dmc.danmu
    # def danmu_fn(msg):
    #     pp('[%s] %s' % (msg['NickName'], msg['Content']))
    @dmc.danmu
    def danmu_fn(msg):
        shell.AppActivate("VisualBoyAdvance")
        time.sleep(.02)
        press('z')
        # test = msg
        # print(test)
    dmc.start(blockThread = True)

    # while 1:

    #     print (test)
    #     readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
    #     temp = str.split(readbuffer, "\n")
    #     readbuffer=temp.pop( )

    #     for line in temp:
    #         x = 0
    #         out = ""
    #         line = str.rstrip(line)
    #         line = str.split(line)

    #         for index, i in enumerate(line):
    #             if x == 0:
    #                 user = line[index]
    #                 user = user.split('!')[0]
    #                 user = user[0:12] + ": "
    #             if x == 3:
    #                 out += line[index]
    #                 out = out[1:]
    #             if x >= 4:
    #                 out += " " + line[index]
    #             x = x + 1

    #         # Respond to ping, squelch useless feedback given by twitch, print output and read to list
    #         if user == "PING: ":
    #             s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
    #         elif user == ":tmi.twitch.tv: ":
    #             pass
    #         elif user == ":tmi.twitch.: ":
    #             pass
    #         elif user == ":%s.tmi.twitch.tv: " % NICK:
    #             pass
    #         else:
    #             try:
    #                 print(user + out)
    #             except UnicodeEncodeError:
    #                 print(user)

    #         # Take in output
    #         if out.lower() == 'up':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('up_arrow')
    #             addtofile()
    #         if out.lower() == 'right':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('right_arrow')
    #             addtofile()
    #         if out.lower() == 'down':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('down_arrow')
    #             addtofile()
    #         if out.lower() == 'left':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('left_arrow')
    #             addtofile()
    #         if out.lower() == 'a':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('z')
    #             addtofile()
    #         if out.lower() == 'b':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('x')
    #             addtofile()
    #         if out.lower() == 'start':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('enter')
    #             addtofile()
    #         if out.lower() == 'select':
    #             shell.AppActivate("%s" % APP)
    #             time.sleep(.02)
    #             press('backspace')
    #             addtofile()

    #         # Write to file for stream view
    #         with open("commands.txt", "w") as f:
    #             for item in commands:
    #                 f.write(item + '\n')

# Democracy Game Mode
if mode.lower() == "democracy":
    with open("lastsaid.txt", "w") as f:
        f.write("")

    count_job = Thread(target = democracy, args = ())
    count_job.start()
    #count_job.join()

    print("Starting %s" % GAME)
    time.sleep(1)
    emulator_job = Thread(target = startemulator, args = ())
    emulator_job.start()

    s=socket.socket( )
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"));
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    print("Sent connected message to channel %s" % CHAT_CHANNEL)

    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer=temp.pop( )

        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1

            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                try:
                    print(user + out)
                except UnicodeEncodeError:
                    print(user)

            # Take in output
            if out.lower() == 'up':
                addtofile()
            if out.lower() == 'right':
                addtofile()
            if out.lower() == 'down':
                addtofile()
            if out.lower() == 'left':
                addtofile()
            if out.lower() == 'a':
                addtofile()
            if out.lower() == 'b':
                addtofile()
            if out.lower() == 'start':
                addtofile()
            if out.lower() == 'select':
                addtofile()

            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')
