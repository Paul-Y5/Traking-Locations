import requests
from requests.structures import CaseInsensitiveDict

url = ('https://api.geoapify.com/v2/places?categories={categories}&filter=rect:{places},{places}&limit=20&apiKey=5151ac446fb14f58b87dda914081fd3d')
response = requests.get(url)
print(url)
print(response.json())

