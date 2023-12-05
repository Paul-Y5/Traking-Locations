import requests

# Base URL for the API
base_url = "https://api.geoapify.com/v2/places?categories="

place = input('Place coordinates: ')
category = input('category: ')
kimit = input('limit: ')
url = (f"{base_url}{category}&filter=rect:{place}&limit=20&apikey=3b217b38a08846b19772470894a181b7")
response = requests.get(url)
print(response.json())