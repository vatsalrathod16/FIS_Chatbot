import pymongo
import pandas as pd
from smtplib import SMTP_SSL as SMTP
from email.message import EmailMessage

try:
    s = SMTP('smtp.gmail.com', 465)
    s.login("realmonster7777@gmail.com", "")
    msg = EmailMessage()
    msg.set_content('This is my message')
    msg['Subject'] = 'Subject'
    msg['From'] = "realmonster7777@gmail.com"
    msg['To'] = "vatsalrathod16@gmail.com"
    s.send_message(msg)
    s.quit()
except Exception:
    print(Exception)
#s.quit()
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['FIS_Chatbot']
col1 = db['locations']
df = "-1"
col = db['Appointment']
#df = col1.find_one({},{'location_name':Location})
df = pd.DataFrame(list(col1.find()))
Location = 'I.S. 117'
try:
    v=df[df['location_name']==Location]
    print(v)
    #fulfillmentText = 'Appointment Booked'
except Exception:
    fulfillmentText = 'please enter valid pantry name'

if(len(v)==0):
    fulfillmentText = 'please enter valid pantry name'
else:
    #fulfillmentText = 'Appointment Booked'
    addDict = {'name' : 'Vatsal',
    'email' : 'vrathod@uncc.edu',
    'phone' : 7043879131,
    'live_appointment' : 'Yes',
    'Appointment_Status' : 'Yes',
    'Appointment_time'  : '7:00',
    'usertype' : 'Donor'}
    col.insert_one(addDict)

