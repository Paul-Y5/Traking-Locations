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
    info_list = []
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    all_info_list = (json_response.get('features'))
    
    for item in all_info_list:
        place_property_dict = item.get('properties')
        place_property_dict.pop('datasource')
        place_property_dict.pop('place_id')
        info_list.append(place_property_dict)
    
    return info_list

def main():
    '''função principal'''
    
    base_url = "https://api.geoapify.com/v2/places?"
    apiKey = '5151ac446fb14f58b87dda914081fd3d'
    
    place = input('Place coordinates (lon,lat): ')
    category = input('Category to search for: ')
    radius = input('Circle radius: ')
    
    url = (f'{base_url}categories={category}&filter=circle:{place},{radius}&bias=proximity:{place}&limit=20&apiKey={apiKey}')
    
    print(get_info(url))

if __name__ == '__main__':
    main()
    



