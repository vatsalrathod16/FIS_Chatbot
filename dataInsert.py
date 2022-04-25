import pymongo
import json
import certifi

'''
firebaseConfig = {"apiKey": "AIzaSyDxHLOgqjQeYUnniDeMI4gsNZWS-Y3XQ1s",
    "authDomain": "fisfirebasedb.firebaseapp.com",
    "projectId": "fisfirebasedb",
    "storageBucket": "fisfirebasedb.appspot.com",
    "messagingSenderId": "81643804817",
    "appId": "1:81643804817:web:300757ad8a36c423b90730",
    "measurementId": "G-7KCX675SD7",
    "databaseURL":"https://fisfirebasedb-default-rtdb.firebaseio.com/"}


firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

data = {"name" : "John", "age":20}
db.push(data)'''

client = pymongo.MongoClient('mongodb+srv://FISChatbot:ZMdaSTA6jkBqKmBo@clusterfis.cd6hr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.get_database('FIS_Chatbot')
collection = db['loc']
requesting = []
with open(r"my_data.json") as f:
    # for jsonObj in f:
        myDict = json.load(f)
        #print(myDict)
        #collection.insert_one(myDict)
print(myDict)
collection.insert_many(myDict)

client.close()