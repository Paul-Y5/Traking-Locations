import requests
from requests.structures import CaseInsensitiveDict

base_url = "https://api.geoapify.com/v2/places?categories="

place = input('Place coordinates: ')
category = input('category: ')
kimit = input('limit: ')

url = (f"{base_url}{category}&bias=proximity:{place}&limit={kimit}&apiKey=5151ac446fb14f58b87dda914081fd3d")
response = requests.get(url)
print(url)
print(response.json())

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.status_code)
print(resp.content)