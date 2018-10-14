from datetime import datetime,time,timedelta
sender=''
receiver=''
times=''
chat=''

def initialize():
    global sender,receiver,times,chat
    configfile=open("config.ini")
    config=configfile.read().split('\n')
    config=[string for string in config if string!='']
    config=[string for string in config if string[0]!='#']
    times=[]
    #setting sender token
    for i in config:
        if ('sender=' in i):
            sender=i.replace('sender=','').strip()
    #setting receiver token
    for i in config:
        if ('receiver=' in i):
            receiver=i.replace('receiver=','').strip()
    #setting up chat
    for i in config:
        if ('chat=' in i):
            chat=i.replace('chat=','').strip()
    for i in config:
        if (('time=' in i) & ( not ('everyminute' in i))):
            temp=i.replace('time=','').strip().split(':')
            times.append(time(int(temp[0]),int(temp[1]),int(temp[2])))
    for i in config:
        if ('time=everyminute' in i):
            times=[]
            for j in range(24):
                for k in range(60):
                    times.append(time(j,k,0))
    return (sender,receiver,chat,times)
