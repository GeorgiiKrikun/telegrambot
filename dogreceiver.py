from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import mimetypes
import subprocess
from datetime import datetime,time,timedelta
import time as tt
import threading

import initialize as init
import receiver as rec
import sender as send

times=[]
sender=''
receiver=''
chat=''
(sender,receiver,chat,times)=init.initialize()

updater = Updater(token=receiver,request_kwargs={'read_timeout': 60, 'connect_timeout': 60})
dispatcher = updater.dispatcher

message_handler=MessageHandler(Filters.all,rec.messagesave2)
dispatcher.add_handler(message_handler)
start_handler = CommandHandler('start',rec.start)
dispatcher.add_handler(start_handler)
senderthreading = threading.Thread(target=send.senderstart,name="senderthread",args=(times,sender,chat))
senderthreading.daemon = True
senderthreading.start()

updater.start_polling()
