from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import mimetypes
from datetime import datetime,time,timedelta
#from threading import Timer
import logging
import subprocess
import time as tt

#chat="@temporalgog"
chat="@DogueCatalogue"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
N=3
times=[]
for i in range(24):
        times.append(time(i,30,0))

#last_file=subprocess.check_output("ls -t description/", shell=True).decode('unicode_escape').split('\n')
#print(len(last_file))
#Sending function

#def imagesend():
	#pictures=subprocess.check_output("ls -t *.jpg", shell=True).split('\n')
	#picturestr=pictures[len(pictures)-2]
	#picture=open(picturestr,"r")
	#updater = Updater(token='473906094:AAHPLdTeCEPLrPPxOLu2mUn9T_Wp1Oi9YaY')
	#bot=updater.bot
	#bot.send_photo(chat_id=chat, photo=picture)
	#print("rm -v "+picturestr)
	#subprocess.call(["rm","-v",picturestr])

def sendstuff():
        #current_number_file=open("current_number","r")
        #current_number=current_number_file.read()
        #current_number_file.close()
        last_file=subprocess.check_output("ls -t description/", shell=True).decode('unicode_escape').split('\n')
        if (len(last_file) <= 1):
                print("no files")
                return
        laststr=last_file[len(last_file)-2]
        print(laststr)
        print(laststr)
        description_file=open("description/"+laststr,"r")
        desc=description_file.read().split('\n')
        description_file.close()
        updater = Updater(token='473906094:AAHPLdTeCEPLrPPxOLu2mUn9T_Wp1Oi9YaY')
        bot=updater.bot
        if (desc[0]=='text'):
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_message(chat_id=chat,text=caption)
        if ((desc[0]=='photo') & (desc[1] != 'cap')):
                picture=open("pictures/"+laststr+'.jpg','rb')
                bot.send_photo(chat_id=chat, photo=picture)
                picture.close();
        if ((desc[0]=='photo') & (desc[1] == 'cap')):
                picture=open("pictures/"+laststr+'.jpg','rb')
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_photo(chat_id=chat, photo=picture,caption=caption)
                picture.close()
        if ((desc[0]=='video') & (desc[1] != 'cap')):
                video=open("videos/"+laststr,'rb')
                bot.send_video(chat_id=chat, video=video)
                video.close();
        if ((desc[0]=='video') & (desc[1] == 'cap')):
                video=open("videos/"+laststr,'rb')
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_video(chat_id=chat, video=video,caption=caption)
                video.close()
        if (len(desc)==3):        
                if ((desc[0]=='doc') & (desc[2] != 'cap')):
                        doc=open("docs/"+laststr+desc[1],'rb')
                        bot.send_document(chat_id=chat, document=doc)
                        doc.close();
                if ((desc[0]=='doc') & (desc[2] == 'cap')):
                        doc=open("docs/"+laststr+desc[1],'rb')
                        caption_file=open("text/"+laststr,"r")
                        caption=caption_file.read()
                        caption_file.close()
                        bot.send_document(chat_id=chat, document=doc,caption=caption)
                        doc.close();
        subprocess.call(["rm","-v","description/"+laststr])                

def timetofulltime(t):
	return t.hour*3600+t.minute*60+t.second

NUtimes=[timetofulltime(i) for i in times]

while True:
	temp=-1;
	currenttime=timetofulltime(datetime.now().time())
	for i in range(len(NUtimes)):
		if currenttime<NUtimes[i]:
			temp=i;
			break
	if (temp > -1):
		print("next iteration in: ",NUtimes[temp]-currenttime);
		tt.sleep(NUtimes[temp]-currenttime);
		sendstuff();
	else:
		print("Putting myself asleep till midnight");
		tt.sleep(24*60*60-currenttime+1);

