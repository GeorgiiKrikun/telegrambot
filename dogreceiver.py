from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import mimetypes
import subprocess
from datetime import datetime,time,timedelta
import time as tt
import threading


times=[]
#times.append(time(6,0,0))
#times.append(time(9,0,0))
#times.append(time(11,0,0))
#times.append(time(13,0,0))
#times.append(time(15,0,0))
#times.append(time(18,30,0))

#for i in range(24):
#        for j in range(60):
#                times.append(time(i,j,0))
sender=''
receiver=''
chat=''
#chat="@DogueCatalogue"





#/start Handling
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="SOBAKI ETO PROSTO BLYAD OHUENNAYA TEMA")



#/stop react
def stop(num):
    subprocess.call(["rm","-v","description/"+num])                

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
           
#MessageHandler
def messagesave(bot, update):
    if ((update.effective_user.username != "goglike") & (update.effective_user.username != "Leenza") & (update.effective_user.username != "kireenkov")):
        bot.send_message(chat_id=update.message.chat_id, text="NAHUI POSHEL, ti ne goglike")
        return
    current_number_file=open("current_number","r")
    current_number=current_number_file.read()
    current_number_file.close()

    if (update.message.text != None ):
        comarr = update.message.text.split(' ')
        if ((comarr[0] == '/stop') & (len(comarr) > 1) ):
            stop(comarr[1])
            bot.send_message(chat_id=update.message.chat_id, text="Task number "+comarr[1] +" stopped")
            return
    
    bot.send_message(chat_id=update.message.chat_id, text="Your task number = "+ current_number+". Use it if you want to stop bot from posting it in form: /stop "+current_number)

    if (len(update.message.photo) != 0):
        desc=open("description/"+current_number,"w")
        desc.write("photo\n")
        incomephotos=update.message.photo
        incomefile=incomephotos[len(incomephotos)-1].get_file();
        incomefile.download(custom_path="pictures/"+current_number+".jpg")
        bot.send_message(chat_id=update.message.chat_id, text="Photo saved")
        if (update.message.caption != None):
            #bot.send_message(chat_id=update.message.chat_id, text="caption "+update.message.caption)
            desc.write("cap")
            cap=open("text/"+current_number,"w")
            cap.write(update.message.caption)
            cap.close()
            bot.send_message(chat_id=update.message.chat_id, text="Caption saved")
    if (update.message.text != None):
        desc=open("description/"+current_number,"w")
        desc.write("text\n")
        desc.close()
        cap=open("text/"+current_number,"w")
        cap.write(update.message.text)
        cap.close()
        bot.send_message(chat_id=update.message.chat_id, text="Text saved")
    if (update.message.document != None):
        print("document")
        desc=open("description/"+current_number,"w")
        desc.write("doc\n")
        incomefile=update.message.document.get_file();
        incomefile.download(custom_path="docs/"+current_number+mimetypes.guess_extension(update.message.document.mime_type))
        bot.send_message(chat_id=update.message.chat_id, text=mimetypes.guess_extension(update.message.document.mime_type)+" saved")
        desc.write(mimetypes.guess_extension(update.message.document.mime_type)+'\n')
        if (update.message.caption != None):
            #bot.send_message(chat_id=update.message.chat_id, text="caption "+update.message.caption)
            desc.write("cap")
            cap=open("text/"+current_number,"w")
            cap.write(update.message.caption)
            cap.close()
            bot.send_message(chat_id=update.message.chat_id, text="Caption saved")
        desc.close()
    if (update.message.video != None):
        print("video")
        desc=open("description/"+current_number,"w")
        desc.write("video\n")
        incomefile=update.message.video.get_file();
        incomefile.download(custom_path="videos/"+current_number)
        bot.send_message(chat_id=update.message.chat_id, text="video saved")
        #desc.write(mimetypes.guess_extension(update.message.document.mime_type)+'\n')
        if (update.message.caption != None):
            #bot.send_message(chat_id=update.message.chat_id, text="caption "+update.message.caption)
            desc.write("cap")
            cap=open("text/"+current_number,"w")
            cap.write(update.message.caption)
            cap.close()
            bot.send_message(chat_id=update.message.chat_id, text="Caption saved")
        desc.close()

    current_number_file=open("current_number","w")
    current_number_file.write(str(int(current_number)+1))
    
    print(update.effective_user.username)

#sender send function
def sendstuff():
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
                sendstuff()
                return
        updater = Updater(token=sender)
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

#sender rotation
def senderstart():
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

initialize()

updater = Updater(token=receiver,request_kwargs={'read_timeout': 60, 'connect_timeout': 60})
dispatcher = updater.dispatcher

NUtimes=[timetofulltime(i) for i in times]


#photo_handler=MessageHandler(Filters.photo,imagesave)
message_handler=MessageHandler(Filters.all,messagesave)
dispatcher.add_handler(message_handler)
start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)
senderthreading = threading.Thread(target=senderstart,name="senderthread")
senderthreading.daemon = True
senderthreading.start()

updater.start_polling()
