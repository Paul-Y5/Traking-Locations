import requests
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder 

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
        if character.isalpha() or character == ',' or character == '.':
            continue
        else:
            print('Formato das categorias incorreto!')
            return False

    users_categories_list = category.replace(',', ' ').split()

    for categories in users_categories_list:
        if categories not in list_of_categories():
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

def print_info(info):
    print("{:^20s} {:^40s} {:^20s} {:^20s} {:^10s} {:^15s}".format("Tipo Atração", "Nome", "Local", "Coordenadas", "Distância", "Fuso-horário"))
    print()
    for dic in info:
        if dic.get('name', '') == '':
            continue
        else:
            tipo_atração = '' 
            for item in dic.get('categories'):
                if '.' in item:
                    continue
                else:
                    tipo_atração += item.capitalize() + ' '

            name = dic.get('name', 'Not found')
            latitude = round(dic.get('lat', 0), 2)
            longitude = round(dic.get('lon', 0), 2)
            local = dic.get('city', 'Not found') 
            distance = dic.get('distance', 'Not found')
            fuso_horario = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
            print(f"{tipo_atração:^20} {name:^40} {local:^20} {str(latitude) + ', ' + str(longitude):^20} {distance:^10} {fuso_horario:^15}")
        
            
def main():
    '''função principal'''
    
    base_url = "https://api.geoapify.com/v2/places?"
    apiKey = '5151ac446fb14f58b87dda914081fd3d'
    
    coords = input('Place coordinates (lat,lon): ').split(',')

    #colocar só quando a verificação for feita. Como a verificação das coordenadas n está a funcionar meti aqui.
    coords1 = str(coords[0])
    coords2 = str(coords[1])
    coords_reverse = coords2 + ',' + coords1

    category = input('Category to search for: ')
    radius = input('Circle radius: ')

    
    
    url = (f'{base_url}categories={category}&filter=circle:{coords_reverse},{radius}&bias=proximity:{coords_reverse}&limit=20&apiKey={apiKey}') if (validate_categories(category) and validate_radius(radius)) else main()
    
    places_info = get_info(url)
    
    print_info(places_info)


if __name__ == '__main__':
    main()
    



