import requests
from requests.structures import CaseInsensitiveDict
# Base URL for the API
base_url = "https://api.geoapify.com/v2/places?categories="

place = input('Place coordinates: ')
category = input('category: ')
kimit = input('limit: ')

url = (f"{base_url}{category}&bias=proximity:{place}&limit={kimit}&apiKey=5151ac446fb14f58b87dda914081fd3d")
headers = CaseInsensitiveDict()
response = requests.get(url, headers=headers)
print(url)
print(response.json())
