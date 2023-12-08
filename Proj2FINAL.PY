import requests
from requests.structures import CaseInsensitiveDict


def categories_list():
    '''função que coloca as categorias de categories.txt numa lista'''
    categories_list = []
    with open('categories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line.strip()
            categories_list.append(line)
    return categories_list

def get_info(url):
    '''Informação útil acerca do local e categorias escolhidas pelo utilizador'''
    places_usefull_info_list = []
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    places_info_list = (json_response.get('features'))
    
    for item in places_info_list:
        item

    return places_info_list

def main():
    '''função principal'''
    base_url = "https://api.geoapify.com/v2/places?categories="
    apiKey = 'apiKey=5151ac446fb14f58b87dda914081fd3d'
    
    place = input('Place coordinates (lon,lat): ')
    category = input('Category to search for: ')
    radius = input('Circle radius: ')
    
    url = (f'{base_url}{category}&filter=circle:{place},{radius}&bias=proximity:{place}&limit=20&{apiKey}')
    
    print(get_info(url))

if __name__ == '__main__':
    main()
    



