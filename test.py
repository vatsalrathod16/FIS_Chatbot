from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_user_agent")
area = "University terrace drive"
city ="Charlotte"
country ="United States"
loc = geolocator.geocode('mira road')
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)