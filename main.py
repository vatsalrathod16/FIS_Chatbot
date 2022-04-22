from flask import Flask, request
from geopy.geocoders import Nominatim
from math import cos, asin, sqrt
import heapq
import pymongo
import pandas as pd


'''
firebaseConfig = {"apiKey": "AIzaSyDxHLOgqjQeYUnniDeMI4gsNZWS-Y3XQ1s",
    "authDomain": "fisfirebasedb.firebaseapp.com",
    "projectId": "fisfirebasedb",
    "storageBucket": "fisfirebasedb.appspot.com",
    "messagingSenderId": "81643804817",
    "appId": "1:81643804817:web:300757ad8a36c423b90730",
    "measurementId": "G-7KCX675SD7",
    "databaseURL":"https://fisfirebasedb-default-rtdb.firebaseio.com/"}'''

# data = {"name" : "John", "age":20}
# db.push(data)
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
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
    print(g)
  elif query_result.get('action') == 'bookAppointment':
    Location = str(query_result.get('parameters').get('any'))
    col1 = db['locations']
    df = "-1"
    #df = col1.find_one({},{'location_name':Location})
    df = pd.DataFrame(list(col1.find()))
    try:
      v=df[df['location_name']==Location]
      print(v)
      #fulfillmentText = 'Appointment Booked'
    except Exception:
      fulfillmentText = 'please enter valid pantry name'

    if(len(v)==0):
      fulfillmentText = 'please enter valid pantry name'
    else:
      fulfillmentText = 'Appointment Booked'
      

  return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }

   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5002)