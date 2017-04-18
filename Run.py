import os

#  生成 配置文件 如果有就退出

settings = []

while True:
    if os.path.isfile("settings.txt"):
        print("过段时间")
        # config = configparser.ConfigParser()
        # config.read("settings.txt")
        # HOST = config.get('Settings', 'HOST')
        # PORT = config.getint('Settings', 'PORT')
        # AUTH = config.get('Settings', 'AUTH')
        # NICK = config.get('Settings', 'USERNAME').lower()
        # APP = config.get('Settings', 'APP')
        # CHAT_CHANNEL = config.get('Settings', 'CHAT_CHANNEL').lower()	
        # command_length = config.getint('Settings', 'LENGTH')
        # QUICK_PRESS = config.getboolean('Settings', 'QUICK_PRESS')
        break
    else:
        print("Let's make you a config file")
        settings.append("; Settings for Twitch Plays Pokemon bot")        
        settings.append("[Settings]\n")
        
        
        settings.append("; Your Twitch Bot's Username")
        print("Your Twitch Bot's Username")
        settings_bot = input("Bot's Username: ")
        settings.append("USERNAME = " + settings_bot + "\n")
        
        settings.append("; Name of the application you run the file from, I suggest VBA")
        print("Name of the application you run the file from, if Visual Boy Advance use VisualBoyAdvance")
        settings_app = input("Application name: ")
        settings.append("APP = " + settings_app + "\n")
        
        settings.append("; The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        print("The maximum number of lines in commands.txt (Useful for showing commands received in stream)")
        settings_length = input("Length: ")
        settings.append("LENGTH = " + settings_length + "\n")
        
        settings.append("; Oh how to explain this...")
        settings.append("; You get the chat command 'Left'")
        settings.append("; You are currently facing right")
        settings.append("; If QUICK_PRESS is true you turn left")
        settings.append("; If QUICK_PRESS is false you turn left and move one square left")
        print("Oh how to explain this...")
        print("You get the chat command 'Left'")
        print("You are currently facing right")
        print("If QUICK_PRESS is true you turn left")
        print("If QUICK_PRESS is false you turn left and move one square left")
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

# 今儿就看到这吧
# Anarchy Game Mode
if mode.lower() == "anarchy":
    with open("lastsaid.txt", "w") as f:
        f.write("")
        
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
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('up_arrow')
                addtofile()
            if out.lower() == 'right':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('right_arrow')
                addtofile()
            if out.lower() == 'down':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('down_arrow')
                addtofile()
            if out.lower() == 'left':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('left_arrow')
                addtofile()
            if out.lower() == 'a':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('z')
                addtofile()
            if out.lower() == 'b':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('x')
                addtofile()
            if out.lower() == 'start':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('enter')
                addtofile()
            if out.lower() == 'select':
                shell.AppActivate("%s" % APP)
                time.sleep(.02)
                press('backspace')
                addtofile()
                
            # Write to file for stream view
            with open("commands.txt", "w") as f:
                for item in commands:
                    f.write(item + '\n')

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
