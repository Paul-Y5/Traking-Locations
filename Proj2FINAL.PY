import requests
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder 

def set_of_categories():
    '''função que coloca as categorias de categories.txt num conjunto'''
    categories_set = set()
    with open('categories.txt', 'r', encoding='utf-8') as file:
        for line in file:
            category = line.strip()
            categories_set.add(category)
        
    return categories_set


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
    valid = True

    for character in place:
        if character.isnumeric() or character == '-' or character == '.':
            continue
        elif character == ',' and virgula_count < 1:
            virgula_count += 1
            continue
        else:
            print('Formato das coordenadas incorreto!')
            valid = False
    
    if valid:
        try:
            coords_list = place.replace(',', ' ').split()
            latitude, longitude = map(float, coords_list)
            
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                pass
            
            else:
                print('Coordenadas fora do intervalo permitido!')
                valid = False
        
        except ValueError:
            print('Formato das coordenadas incorreto!')
            valid = False
    else:
        pass
    
    return valid


def validate_categories(category):
    '''Verifica se as categorias estão de acordo com o pedido na URL'''
    valid = True
    for character in category:
        if character.isalpha() or character == ',' or character == '.':
            continue
        else:
            print('Formato das categorias incorreto!')
            valid = False

    users_categories_list = category.replace(',', ' ').split()

    if valid == False:
        pass
    else:
        for categories in users_categories_list:
            if categories not in set_of_categories():
                print('Formato das categorias incorreto!')
                valid = False
                break
       
    return valid


def validate_radius(radius):
    '''Verifica se o raio estão de acordo com o pedido na URL'''
    not_num = 0
    ponto_count = 0
    valid = True
    for num in radius:
        if num.isnumeric() or (num == '.' and ponto_count < 2):
            continue
        else:
            not_num += 1
    
    if not_num == 0:
        pass
    else:
        print('Valor para raio não suportado!')
        valid = False
    
    return valid


def print_info(info, category):
    count = 0
    distancia_total = 0
    if len(info) == 0:
        print('Nenhuma informação encontrada sobre o local!') 
    else:
        print("{:^40s} {:^40s} {:^20s} {:^20s} {:^10s} {:^15s}".format("Tipo Atração", "Nome", "Local", "Coordenadas", "Distância", "Fuso-horário"))
        print()
        for dic in info:
            if dic.get('name', '') == '':
                continue
            else:
                users_categories_list = category.replace(',', ' ').split()
                tipo_atração = '' 
                
                for item in dic.get('categories'):
                    if '.' in item:
                        continue
                    else:
                        tipo_atração += (item.capitalize() + ', ') if (item in users_categories_list) else ''
                
                if tipo_atração[-2] == ',':
                    tipo_atração = tipo_atração[:-2] + tipo_atração[-1]

                name = dic.get('name')
                latitude = round(dic.get('lat', 0), 2)
                longitude = round(dic.get('lon', 0), 2)
                local = dic.get('city', 'Not found') 
                distance = dic.get('distance', 'Not found')
                fuso_horario = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
                print(f"{tipo_atração:^40} {name:^40} {local: ^20} {str(latitude) + ', ' + str(longitude):^20} {distance:^10} {fuso_horario:^15}")
                count += 1
                distancia_total += distance
        print(f'Foram encontradas {count} atrações segundo as categorias indicadas!')
        print(f'A distância média às atrações é de {distancia_total / count} m')            
def main():
    '''função principal'''
    
    base_url = "https://api.geoapify.com/v2/places?"
    apiKey = '5151ac446fb14f58b87dda914081fd3d'
    
    coords = input('Place coordinates (lat,lon): ')
    category = input('Category to search for: ')
    radius = input('Circle radius: ')

    if validate_coords(coords):
        coords_list = coords.split(',')
        coords1 = str(coords_list[0])
        coords2 = str(coords_list[1])
        coords_reverse = coords2 + ',' + coords1
        print(coords_reverse)

    url = (f'{base_url}categories={category}&filter=circle:{coords_reverse},{radius}&bias=proximity:{coords_reverse}&limit=20&apiKey={apiKey}') if (validate_coords(coords) and validate_categories(category) and validate_radius(radius)) else main()
    
    places_info = get_info(url)
    
    print_info(places_info, category)


if __name__ == '__main__':
    main()
    



