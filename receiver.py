from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters


#/start Handling
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="SOBAKI ETO PROSTO BLYAD OHUENNAYA TEMA")

#/stop react
def stop(num):
    subprocess.call(["rm","-v","description/"+num])                
   
def messagesave2(bot, update):
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
    
    if (update.message.media_group_id == None):    
            if (update.message.text != None):
                desc=open("description/"+current_number,"w")
                desc.write("text\n")
                desc.close()
                cap=open("text/"+current_number,"w")
                cap.write(update.message.text)
                cap.close()
                bot.send_message(chat_id=update.message.chat_id, text="Text saved")  
            elif (len(update.message.photo) != 0):
                desc=open("description/"+current_number,"w")
                desc.write("photo\n")
                incomephotos=update.message.photo
                incomefile=incomephotos[len(incomephotos)-1].get_file();
                bot.send_message(chat_id=update.message.chat_id, text="Photo saved")
            elif ( update.message.document != None):
                desc=open("description/"+current_number,"w")
                desc.write("doc\n")
                incomefile=update.message.document.get_file();
                bot.send_message(chat_id=update.message.chat_id, text="file saved")
            elif ( update.message.video != None ):
                desc=open("description/"+current_number,"w")
                desc.write("video\n")
                incomefile=update.message.video.get_file();
                bot.send_message(chat_id=update.message.chat_id, text="video saved")
            if (update.message.caption != None):
                #bot.send_message(chat_id=update.message.chat_id, text="caption "+update.message.caption)
                desc.write("cap")
                cap=open("text/"+current_number,"w")
                cap.write(update.message.caption)
                cap.close()
                bot.send_message(chat_id=update.message.chat_id, text="Caption saved")
            desc.write('\n'+incomefile.file_id)
            desc.close()
            current_number_file=open("current_number","w")
            current_number_file.write(str(int(current_number)+1))        
    else:
            if (len(update.message.photo) != 0):
                desc=open("description/"+current_number,"w")
                desc.write("photo\n")
                incomephotos=update.message.photo
                incomefile=incomephotos[len(incomephotos)-1].get_file();
                bot.send_message(chat_id=update.message.chat_id, text="Photo saved")
            elif ( update.message.document != None):
                desc=open("description/"+current_number,"w")
                desc.write("doc\n")
                incomefile=update.message.document.get_file();
                bot.send_message(chat_id=update.message.chat_id, text="file saved")
            elif ( update.message.video != None ):
                desc=open("description/"+current_number,"w")
                desc.write("video\n")
                incomefile=update.message.video.get_file();
                bot.send_message(chat_id=update.message.chat_id, text="video saved")
            if (update.message.caption != None):
                #bot.send_message(chat_id=update.message.chat_id, text="caption "+update.message.caption)
                desc.write("cap")
                cap=open("text/"+current_number,"w")
                cap.write(update.message.caption)
                cap.close()
                bot.send_message(chat_id=update.message.chat_id, text="Caption saved")
            desc.write('\n'+incomefile.file_id)
            desc.write('\n'+update.message.media_group_id)
            desc.close()
            current_number_file=open("current_number","w")
            current_number_file.write(str(int(current_number)+1))
    
    print(update.effective_user.username)
    
    


