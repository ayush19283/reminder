from telethon import TelegramClient,events,sync
from telethon.sessions import StringSession
import psycopg2
from datetime import datetime
import requests
import time
import threading
import pytz
import os 

conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cur=conn.cursor()

api_id=os.environ.get('api_id')
api_hash=os.environ.get('api_hash')
str_sess=os.environ.get('str_sess')


client = TelegramClient(StringSession(str_sess),
                    api_id,
                    api_hash,
                    )
##client.start()



@client.on(events.NewMessage)
async def handler(event):
    message=''
    sender = await event.get_sender()
    if event.raw_text=='/set':
            await event.reply('enter the title and date (YY-MM-DD) and time (HH:MM)')

    message_crt_obj =await event.get_reply_message()
   


        
        

    message = message_crt_obj.raw_text
##        print(message)
##        try:
    if message=='enter the title and date (YY-MM-DD) and time (HH:MM)':
        print(1)
        a=event.message.message
##        message=''

        
        
    
    if '-' and ':' in a:
        
            
        c=a.split(' ')
        s=event.sender.id
        tit1=c[0:len(c)-2]
        tit=' '.join([i for i in tit1])
        
        
        f=c[len(c)-2:len(c)]
        print(f[0])
        print(f[1])
        
        tm=f[0]+' '+f[1]
        
        local = pytz.timezone("Asia/Kolkata")
        naive = datetime.strptime(tm, "%Y-%m-%d %H:%M")
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        print(utc_dt)
        

        cur.execute(f"insert into db (chat_id,done,timedate,title) values ({s},0,'{utc_dt}','{tit}')")
                   
        conn.commit()
    
        print('done')
    else:
        pass
        
    
   
ci=[]

def calc():
    while 1:
        time.sleep(0.4)
        try:
            cur.execute('select chat_id,title from db where timedate<now() and done=0')
            ci.extend(cur.fetchall())
            conn.commit()
            
            if ci:
                tri()
##            if ci:
##                for i in ci:
##                    li.append(i[0])
##                    lj.append(i[1])
                    
                   
        except psycopg2.ProgrammingError:
            print('pgerror')

def tri():

    for i in ci:
        
        requests.get(f"https://api.telegram.org/bot2037652357:AAGJwNlXY2WBCeQTYNtEBbkmAxWbDjQ-zTg/sendMessage?chat_id={i[0]}&text=reminder-for-'{i[1]}'")

        cur.execute(f"update db set done=1 where chat_id={i[0]} and timedate<now()")
        conn.commit()
    
        ci.remove(i)

            
        

T3=threading.Thread(target=calc)


T3.start()
    



    
        
   

        
        


client.start()
client.run_until_disconnected()

