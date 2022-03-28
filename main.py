from flask import Flask, request
from geopy.geocoders import Nominatim
import pymongo


firebaseConfig = {"apiKey": "AIzaSyDxHLOgqjQeYUnniDeMI4gsNZWS-Y3XQ1s",
    "authDomain": "fisfirebasedb.firebaseapp.com",
    "projectId": "fisfirebasedb",
    "storageBucket": "fisfirebasedb.appspot.com",
    "messagingSenderId": "81643804817",
    "appId": "1:81643804817:web:300757ad8a36c423b90730",
    "measurementId": "G-7KCX675SD7",
    "databaseURL":"https://fisfirebasedb-default-rtdb.firebaseio.com/"}
# data = {"name" : "John", "age":20}
# db.push(data)
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['FIS_Chatbot']
collection = db['locations']

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
  elif query_result.get('action') == 'LocationName':
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

   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5002)