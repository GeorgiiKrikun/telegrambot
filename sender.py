from telegram.ext import Updater
#from telegram.ext import Bot
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from datetime import datetime,time,timedelta
#from threading import Timer
import logging
import subprocess
import time as tt

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
N=3

times = [time(10,40,0),time(10,40,30),time(10,41,0),time(10,41,45)]

#Sending function

def imagesend():
	pictures=subprocess.check_output("ls -t *.jpg", shell=True).split('\n')
	picturestr=pictures[len(pictures)-2]
	picture=open(picturestr,"r")
	updater = Updater(token='473906094:AAHPLdTeCEPLrPPxOLu2mUn9T_Wp1Oi9YaY')
	bot=updater.bot
	bot.send_photo(chat_id="@temporalgog", photo=picture)
	print("rm -v "+picturestr)
	subprocess.call(["rm","-v",picturestr])

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
		imagesend();
	else:
		print("Putting myself asleep till midnight");
		tt.sleep(24*60*60-currenttime+1);

