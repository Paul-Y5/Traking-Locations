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
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    places_info_dict = (json_response.get('features'))
    return places_info_dict

def main():
    '''função principal'''
    base_url = "https://api.geoapify.com/v2/places?categories="
    place = input('Place coordinates (lon,lat): ')
    category = input('Category to search for: ')
    radius = input('Circle radius: ')
    apiKey = 'apiKey=5151ac446fb14f58b87dda914081fd3d'
    url = (f'{base_url}{category}&filter=circle:{place},{radius}&bias=proximity:{place}&limit=20&{apiKey}')
    print(get_info(url))

if __name__ == '__main__':
    main()
    



