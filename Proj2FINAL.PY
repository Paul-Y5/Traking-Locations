import requests
from requests.structures import CaseInsensitiveDict

base_url = "https://api.geoapify.com/v2/places?categories="


place = input('Place coordinates: ')
category = input('category: ')
radius = input('Radius')
url = (f'https://api.geoapify.com/v2/places?categories={category}&filter=circle:{place},{radius}&bias=proximity:{place}&limit=20&apiKey=5151ac446fb14f58b87dda914081fd3d')
response = requests.get(url)
print(url)
print(response.json())

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.status_code)
print(resp.content)


list_categories = []
with open('categories.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line.strip()
        list_categories.append(line)

print(list_categories)
