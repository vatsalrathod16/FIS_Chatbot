import streamlit as st
import hashlib
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

from pymongo import MongoClient
from geopy.geocoders import Nominatim

import pandas as pd

from math import cos, asin, sqrt
import heapq

client = MongoClient('mongodb+srv://FISChatbot:ZMdaSTA6jkBqKmBo@clusterfis.cd6hr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mydb1 = client["FIS_Chatbot"]
df = pd.DataFrame.from_records(client.FIS_Chatbot.locations.find())

def login_user(username,p):
	mydb = mydb1.User		
	login_user = mydb.find_one({'email' : username})
	if login_user:
		if login_user['password']==p:
			return True
	return False


def findClosest(address):
	geolocator = Nominatim(user_agent="my_user_agent")
	loc = geolocator.geocode(address)
	return loc

def Signup(new_user, new_password, customer_type, cust_number, f_name, l_name, address):
		mydb = mydb1.User		
		z=[i for i in mydb.find({'name' : new_user})]
		if len(z)<1:
			mydict = {"email": new_user, "password": new_password, "usertype": customer_type, "Number": cust_number, "first_name": f_name, "last_name": l_name, "address":address }
			x = mydb.insert_one(mydict)
			return True
		return False	

def distance(lat1, lon1, lat2, lon2, df):
    # df=pd.read_json('data.json')
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))


def distance1(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)* p)/2 + cos(lat1* p)* cos(lat2* p) * (1-cos((lon2-lon1)* p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(v, data, df):
    r=[]
    for i in range(len(v)):
        r.append([distance(v[i][0],v[i][1], data[0],data[1], df), i])
    heapq.heapify(r)
    return heapq.nsmallest(5, r)

def homepage():
	# st.markdown("<h1 style='text-align: center; color: white;'>Corelation Visualizer using Knowledge Graph</h1>")
	st.markdown("<p style='text-align: center; color: grey;'>Many people do not have the resources to meet their basic needs, challenges that increase a family’s risk of food insecurity. In 2020, an estimated 1 in 8 Americans were food insecure, equating to over 38 million Americans, including almost 12 million children. Food insecurity does not only exist in families below the poverty line, it also exists in families that live above the poverty line. There are lots of factors that contribute to food insecurity in families; Lay-offs at work, unexpected car maintenance, or an accident on the job can suddenly force a family to choose between buying food and paying bills. This can lead to serious health conditions in individuals. Our chatbot aims to connect food donors to nearby food pantries and soup kitchens to donate food and receiver to check nearby places to pick up food.</p><p style='text-align: center; color: grey;'>The webapp is created primarily to provide a platform in which the chatbot could be integrated. The webapp features include account creation, login, editing credentials and provides an interface allowing the user to interact with the chatbot based on their needs</p>", unsafe_allow_html=True)


def main():

	st.markdown("<h1 style='text-align: center; color: white;'>FIS App</h1>", unsafe_allow_html=True)
	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("",menu)

	if choice == "Home":
		homepage()
		# print(pd.DataFrame(cursor))
		st.sidebar.markdown("<p style='text-align: justify; color: grey;'>This is a webapp built on Streamlit to allow users to register and book appointments based on date.</p>", unsafe_allow_html=True)
		st.sidebar.markdown("<p style='text-align: left; color: white;'>Stack Used</p>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>Python</li>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>StreamLit</li>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>MongoDB</li>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>Pandas</li>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>Google DialogFLow</li>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>Flask</li>", unsafe_allow_html=True)
		st.sidebar.markdown("<li style='text-align: left; color: grey;'>Ngrok</li>", unsafe_allow_html=True)

	elif choice == "Login":
		username = st.sidebar.text_input("Enter Email")
		password = st.sidebar.text_input("Enter Password",type='password')
		if st.sidebar.checkbox("Login"):
			# st.markdown("<h1 style='text-align: center; color: white;'>Welcome!!</h1>", unsafe_allow_html=True)
			result = login_user(username,password)
			if result:
				st.balloons()
				mydb = mydb1.User
				_user = mydb.find_one({'email' : username})
				c1, c2, c3=st.columns([3,0.3,1.7])
				with c1:
					st.write("Welcome to the FIS ChatBot System", _user['first_name'], ". We have created the chatbot to help users like you, to simplify the process of accepting and donating based on your requirements")
					st.write("Your current Location is: ", _user['address'])

					html_str = f"""
						<style>
						p.a {{
						  font: bold {15}px;
						}}
						</style>
						<h5 class="a">Want to Donate? Here are 5 nearby pantries</h5>
						"""
					st.markdown(html_str, unsafe_allow_html=True)
					st.write("")
					# st.write(_user['address'])
					coord=findClosest(_user['address'])

					tempDataList = [[i,j] for i,j in zip(df.location_latitude, df.location_longitude)]
					# print(tempDataList)
					res=closest(tempDataList,[coord.latitude, coord.longitude], df)
					# st.write(res)
					y=[str(df.iloc[i[1]].location_name) for i in res]

					for i in range(len(y)):
						html_str = f"""
						<style>
						p.a {{
						  font: bold {10}px;
						}}
						</style>
						<li class="a">{y[i]}</li>
						"""
						st.markdown(html_str, unsafe_allow_html=True)
				with c3:
					v()
				# st.button()


			else:
				st.sidebar.warning("Incorrect Email/Password")

	elif choice == "SignUp":

		with st.form("my_form"):
			c1, c2, c3=st.columns(3)
			with c1:
				f_name=st.text_input("First Name")
			with c2:
				l_name=st.text_input("Last Name")
			with c3:
				customer_type=st.selectbox("Select type: ", ['Donor', 'Reciever'])
			c4, c5=st.columns(2)
			with c4:
				new_user = st.text_input("Enter Email")
			with c5:
				cust_number=st.text_input("Enter Phone Number")
			address=st.text_input("Enter address")

			new_password = st.text_input("Password",type='password')
			cnfrm=st.text_input("Confirm Password", type='password')

			_,_,d,_,_=st.columns(5)
			if d.form_submit_button("Signup"):
				# if is_email(new_user, check_dns=True):
					if len(f_name) < 1 or len(l_name)<1 or len(customer_type)<1 or len(new_user)< 1 or len(address)<1:
						st.sidebar.warning("Enter all fields")
					elif new_password != cnfrm:
						st.sidebar.warning("Passwords don't match")
					elif Signup(new_user, new_password, customer_type, cust_number, f_name, l_name, address):
						st.success("You have successfully created a valid Account")
						st.info("Go to Login Menu to login")
					else:
						st.sidebar.warning("Already in use")

def v():
	components.html(
	'''
	<script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
<df-messenger
  intent="WELCOME"
  chat-title="FIS_CHATBOT"
  agent-id="7bfc1290-a60c-45d2-823a-9937b55a53e1"
  language-code="en"
></df-messenger>
	''',
	height=350
	)

main()



