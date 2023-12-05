import requests

# Base URL for the API
base_url = "https://api.geoapify.com/v2/places?categories="

place = input('Place coordinates: ')
category = input('category: ')
kimit = input('limit: ')
url1 = 'https://api.geoapify.com/v2/places?categories=activity&filter=rect:16.17903071551638,48.28499347053008,16.556767855560192,48.0623697740825&limit=20&apiKey=3b217b38a08846b19772470894a181b7'
url = (f"{base_url}{category}&filter=rect:{place}&limit=500&apikey=3b217b38a08846b19772470894a181b7")
response = requests.get(url)
print(response.json())