from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import mimetypes
import subprocess
from datetime import datetime,time,timedelta
import time as tt
import threading

#sender send function
def sendstuff(sender,chat):
        #current_number_file=open("current_number","r")
        #current_number=current_number_file.read()
        #current_number_file.close()
        last_file=subprocess.check_output("ls -t description/", shell=True).decode('unicode_escape').split('\n')
        if (len(last_file) <= 1):
                print("no files")
                return
        laststr=last_file[len(last_file)-2]
        description_file=open("description/"+laststr,"r")
        desc=description_file.read().split('\n')
        description_file.close()
        if ((desc[0] != "photo") & (desc[0] != "text") & (desc[0] != "doc") & (desc[0] != "video")):
                bot.send_message(chat_id="@goglike",text="something is wrong with " + laststr)
                subprocess.call(["rm","-v","description/"+laststr])
                sendstuff(sender,chat)
                return
        updater = Updater(token=sender)
        bot=updater.bot
        if (desc[0]=='text'):
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_message(chat_id=chat,text=caption)
        if ((desc[0]=='photo') & (desc[1] != 'cap')):
                bot.send_photo(chat_id=chat, photo=desc[2])
        if ((desc[0]=='photo') & (desc[1] == 'cap')):
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_photo(chat_id=chat, photo=desc[2],caption=caption)
        if ((desc[0]=='doc') & (desc[1] != 'cap')):
                bot.send_document(chat_id=chat, document=desc[2])
        if ((desc[0]=='doc') & (desc[1] == 'cap')):
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_document(chat_id=chat, document=desc[2],caption=caption)
        if ((desc[0]=='video') & (desc[1] != 'cap')):
                bot.send_video(chat_id=chat, video=desc[2])
        if ((desc[0]=='video') & (desc[1] == 'cap')):
                caption_file=open("text/"+laststr,"r")
                caption=caption_file.read()
                caption_file.close()
                bot.send_video(chat_id=chat, video=desc[2], caption=caption)
        
        #if (len(desc)==3):        
        #        if ((desc[0]=='doc') & (desc[2] != 'cap')):
        #                doc=open("docs/"+laststr+desc[1],'rb')
        #                bot.send_document(chat_id=chat, document=doc)
        #                doc.close();
        #        if ((desc[0]=='doc') & (desc[2] == 'cap')):
        #                doc=open("docs/"+laststr+desc[1],'rb')
        #                caption_file=open("text/"+laststr,"r")
        #                caption=caption_file.read()
        #                caption_file.close()
        #                bot.send_document(chat_id=chat, document=doc,caption=caption)
        #                doc.close();
        subprocess.call(["rm","-v","description/"+laststr])                

def timetofulltime(t):
	return t.hour*3600+t.minute*60+t.second

#sender rotation
def senderstart(times,sender,chat):
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
		        sendstuff(sender,chat);
	        else:
		        print("Putting myself asleep till midnight");
		        tt.sleep(24*60*60-currenttime+1);


