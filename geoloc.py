# importing geopy library
from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

# entering the location name
getLoc_store = loc.geocode("140 литБ, Московская улица, Краснодар, Краснодарский край, Россия")
getLoc_delivery = loc.geocode("104/1, Селезнёва, Краснодар, Краснодарский край, Россия")
# printing address
print(getLoc_store.address)

latitude = str(getLoc_store.latitude)
longitude = str(getLoc_store.longitude)   
# printing latitude and longitude
location = loc.geocode(latitude + "," + longitude)
 
# Display location
print("\nLocation of the given Latitude and Longitude:")
print(location)


url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&z=10&pt={longitude},{latitude},pm2bl"
print(url)


latitude = str(getLoc_delivery.latitude)
longitude = str(getLoc_delivery.longitude)   
# printing latitude and longitude
# printing latitude and longitude
location = loc.geocode(latitude + "," + longitude)
 
# Display location
print("\nLocation of the given Latitude and Longitude:")
print(location)

url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&z=10&pt={longitude},{latitude},pm2bl"
print(url)