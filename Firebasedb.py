import pyrebase


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
db.push(data)