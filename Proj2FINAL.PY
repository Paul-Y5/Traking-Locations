import requests
from requests.structures import CaseInsensitiveDict

def list_of_categories():
    '''função que coloca as categorias de categories.txt numa lista'''
    categories_list_n = []
    with open('categories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line.strip().split(' ')
            categories_list_n.append(line)
        
        categories_list = [s.replace('\n', '') for s in categories_list_n]
    
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

def validate_coords(place):
    '''Verifica se as coordenadas estão de acordo com o pedido na URL'''
    virgula_count = 0

    for character in place:
        if character.isnumeric():
            continue
        elif character == ',' and virgula_count < 1:
            virgula_count += 1
            continue
        else:
            print('Formato das coordenadas incorreto!')
            return False
    
    coords_list = place.replace(',', ' ').split()
    
    if float(coords_list[0]) < -90 or float(coords_list[0]) > 90 or (float(coords_list[1]) < -90 or float(coords_list[1]) > 90):
        print('Formato das coordenadas incorreto!')
        return False
    else:
        return True


def validate_categories(category):
    '''Verifica se as categorias estão de acordo com o pedido na URL'''
    for character in category:
        if character.isalpha():
            continue
        elif character == ',' or character == '.':
            continue
        else:
            print('Formato das categorias incorreto!')
            return False

    users_categories_list = category.replace(',', ' ').split()

    for categories in users_categories_list:
        if categories not in list_of_categories():
            print(list_of_categories())
            print(users_categories_list)
            print(categories in list_of_categories())
            print('Formato das categorias incorreto!')
            return False
        else:
            return True


def validate_radius(radius):
    '''Verifica se o raio estão de acordo com o pedido na URL'''
    not_num = 0
    
    for num in radius:
        if num.isnumeric():
            continue
        else:
            not_num += 1
    
    if not_num == 0:
        return True
    else:
        print('Valor para raio não suportado!')
        return False
    
    
def main():
    '''função principal'''
    
    base_url = "https://api.geoapify.com/v2/places?"
    apiKey = '5151ac446fb14f58b87dda914081fd3d'
    
    place = input('Place coordinates (lon,lat): ')
    category = input('Category to search for: ')
    radius = input('Circle radius: ')

    
    
    url = (f'{base_url}categories={category}&filter=circle:{place},{radius}&bias=proximity:{place}&limit=20&apiKey={apiKey}') if (validate_coords(place) and validate_categories(category) and validate_radius(radius)) else main()
    
    places_info = get_info(url)
    
    for item in places_info:
        print(item)
        print('-------------------------------------------------')


if __name__ == '__main__':
    main()
    



