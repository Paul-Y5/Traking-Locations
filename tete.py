import requests
from requests.structures import CaseInsensitiveDict
# Base URL for the API
base_url = "https://api.geoapify.com/v2/places?categories="

place = input('Place coordinates: ')
category = input('category: ')
kimit = input('limit: ')

url = (f"{base_url}{category}&filter=rect:{place}&limit={kimit}&apikey=3b217b38a08846b19772470894a181b7")
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
response = requests.get(url, headers=headers)
print(url)
print(response.json())