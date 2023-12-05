import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.geoapify.com/v2/places?categories=activity&filter=rect:16.17903071551638,48.28499347053008,16.556767855560192,48.0623697740825&limit=20&apiKey=3b217b38a08846b19772470894a181b7"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.status_code)
print(resp.content)