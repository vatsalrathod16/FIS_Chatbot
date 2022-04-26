from flask import Flask, request
from geopy.geocoders import Nominatim
from math import cos, asin, sqrt
import heapq
import pymongo
import pandas as pd
from smtplib import SMTP_SSL as SMTP
from email.message import EmailMessage


client = pymongo.MongoClient('mongodb+srv://FISChatbot:ZMdaSTA6jkBqKmBo@clusterfis.cd6hr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['FIS_Chatbot']


app = Flask(__name__)
@app.route('/') # this is the home page route
def hello_world(): # this is the home page function that generates the page code
  return "hello"
  
@app.route('/getLocation',methods=['GET','POST'])
def getLocation():
  req = request.get_json(silent=True, force=True)
  query_result = req.get('queryResult')
  if query_result.get('action') == 'LocationName':
    Location = str(query_result.get('parameters').get('any'))
    geolocator = Nominatim(user_agent="my_user_agent")
    area = "University terrace drive"
    city ="Charlotte"
    country ="United States"
    loc = geolocator.geocode(Location)
    fulfillmentText = "latitude is :-"+str(loc.latitude)+"\nlongtitude is:-"+str(loc.longitude)
    return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)* p)/2 + cos(lat1* p)* cos(lat2* p) * (1-cos((lon2-lon1)* p)) / 2
    return 12742 * asin(sqrt(hav))


@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  fulfillmentText = ''
  sum = 0
  query_result = req.get('queryResult')
  if query_result.get('action') == 'sub.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    sum = str(num1 + num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The sum of the two numbers is '+sum
  elif query_result.get('action') == 'multiply.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    product = str(num1 * num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The product of the two numbers is '+product
  elif query_result.get('action') == 'LocationList':
    Location = str(query_result.get('parameters').get('any'))
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(Location)
    fulfillmentText = "latitude is :-"+str(loc.latitude)+"\nlongtitude is:-"+str(loc.longitude)
  elif query_result.get('action') == 'LocationName':
    print("hello")
    Location = str(query_result.get('parameters').get('any'))
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(Location)
    userLat = loc.latitude
    userLong = loc.longitude
    fulfillmentText = []
    r=[]
    col = db['locations']
    df = pd.DataFrame(list(col.find()))
    print(df)
    v = [[i,j] for i,j in zip(df.location_latitude, df.location_longitude)]
    for i in range(len(v)):
        r.append([distance(v[i][0],v[i][1], userLat,userLong), i])
    heapq.heapify(r)
    fulfillmentText = list(heapq.nsmallest(5, r))
    #fulfillmentText=5
    # print()
    m=[str(df.iloc[i[1]].location_name) for i in heapq.nsmallest(5, r)]
    fulfillmentText="\n ".join(m)
  elif query_result.get('action') == 'bookAppointment':
    Location = str(query_result.get('parameters').get('any'))
    col1 = db['locations']
    df = "-1"
    df = pd.DataFrame(list(col1.find()))
    try:
      v=df[df['location_name']==Location]
      print(v)
    except Exception:
      fulfillmentText = 'please enter valid pantry name'
    if(len(v)==0):
      fulfillmentText = 'please enter valid pantry name'
    else:
      fulfillmentText = 'Confirm Location'
  elif query_result.get('action') == 'locationconfirm':
    Location = str(query_result.get('parameters').get('any'))
    fulfillmentText = 'Confirm Email Address'
  elif query_result.get('action') == 'CheckStatus':
    #print('hello')
    input = str(query_result.get('parameters').get('any'))
    location = input[0]
    dt = input[1]
    col = db['Appointment']
    df = pd.DataFrame(list(col.find()))
    donor_count=len(df[(df['location_name']==location) & (df['date']==dt) & (df['usertype']=='Donor')])
    recieve_count=len(df[(df['location_name']==location) & (df['date']==dt) & (df['usertype']=='Donor')])
    fulfillmentText = 'Donor count ='+str(donor_count)+'\n Reciever count='+str(recieve_count)
  elif query_result.get('action') == 'CheckStatusPantry':
    #print('hello')
    dt = str(query_result.get('parameters').get('any'))
    #location = input[0]
    #dt = input[1]
    col = db['Appointment']
    df = pd.DataFrame(list(col.find()))
    fulfillmentText = df[(df['date']==dt) & (df['usertype']=='Donor')]
    fulfillmentText = dict(fulfillmentText.groupby('location_name').size())
    for i in fulfillmentText:
      temp=i+' : '+str(fulfillmentText[i])+'\n'
    fulfillmentText = temp
    print(fulfillmentText)
    #fulfillmentText = 'hello'
  elif query_result.get('action') == 'CheckStatusPantry':
    try:
      s = SMTP('smtp.gmail.com', 465)
      s.login("realmonster7777@gmail.com", "youmonster")
      msg = EmailMessage()
      msg.set_content('This is my message')
      msg['Subject'] = 'Subject'
      msg['From'] = "realmonster7777@gmail.com"
      msg['To'] = "vatsalrathod16@gmail.com"
      s.send_message(msg)
      s.quit()
    except Exception:
      print(Exception)
  elif query_result.get('action') == 'BookAppointment':
    
    location_name = str(query_result.get('parameters').get('any'))
    email = str(query_result.get('parameters').get('email'))
    dt = str(query_result.get('parameters').get('date'))
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
        'email' : email,
        'phone' : 7043879131,
        'live_appointment' : 'Yes',
        'Appointment_Status' : 'Yes',
        'Appointment_time'  : '7:00',
        'usertype' : 'Donor'}
        print(col.insert_one(addDict))

    fulfillmentText = 'Appointment booked! kindly check your email'
    try:
      # print('Hello')
      s = SMTP('smtp.gmail.com', 465)
      s.login("realmonster7777@gmail.com", "")
      msg = EmailMessage()
      message_content = 'Pantry Location : '+location_name+'\n'+'date :'+dt
      msg.set_content(message_content)
      msg['Subject'] = 'Pantry Appointment Booked!'
      msg['From'] = "realmonster7777@gmail.com"
      msg['To'] = email
      s.send_message(msg)
      s.quit()
    except Exception:
      print(Exception)  
    

#s.quit()
  return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }

'''app = Flask(__name__)
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
  req = request.get_json(silent=True, force=True)
  fulfillmentText = ''
  sum = 0
  query_result = req.get('queryResult')
  print(query_result)
  if query_result.get('action') == 'sub.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    sum = str(num1 + num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The sum of the two numbers is '+sum
  elif query_result.get('action') == 'multiply.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    product = str(num1 * num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The product of the two numbers is '+product

  elif query_result.get('action')=='book.custom':
    def distance(lat1, lon1, lat2, lon2, df):
        # df=pd.read_json('data.json')
        p = 0.017453292519943295
        hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(hav))

    def closest(v, data, df):
        r=[]
        for i in range(len(v)):
            r.append([distance(v[i][0],v[i][1], data[0],data[1], df), i])
        heapq.heapify(r)
        return heapq.nsmallest(5, r)

    print('1111111')
    num1 = (query_result.get('parameters').get('any'))
    print(num1)
    df=pd.read_json('data.json')
    print(df)
    tempDataList = [[i,j] for i,j in zip(df.location_latitude, df.location_longitude)]
    print(tempDataList)
    res=closest(tempDataList,[39.7622290, -86.1519750], df)
    y=[str(df.iloc[i[1]].location_name) for i in res]

    fulfillmentText = 'The product of the two numbers is '+ "".join(y)
    print(fulfillmentText)

  return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }'''
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5002)
