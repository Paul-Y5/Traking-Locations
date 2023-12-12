import requests
from time import sleep
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder 

def set_of_categories():
    '''função que coloca as categorias de categories.txt num conjunto'''
    categories_set = set()                                          # criar um set vazio
    with open('categories.txt', 'r', encoding='utf-8') as file:     # abrir ficheiro "categories.txt"
        for line in file:                                           # iterar pelas linhas
            category = line.strip()                                 # remover tudo o que vier no final da linha
            categories_set.add(category)                            # adicionar categoria ao set
        
    return categories_set                                           # returnar set


def get_info(url):
    '''Informação útil acerca do local e categorias escolhidas pelo utilizador'''
    info_list = []                                      # lista onde será colocada a informação obtida pela API 
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(url, headers=headers)
    json_response = response.json()                     # colocar informação num dicionário
    all_info_list = (json_response.get('features'))     # selecionar apenas a informação relativa ás 'features' do local
    
    for item in all_info_list:
        place_property_dict = item.get('properties')    # obter o valor das properties
        place_property_dict.pop('datasource')           # remover datasource
        place_property_dict.pop('place_id')             # remover place id 
        info_list.append(place_property_dict)           # adicionar dicionário com as informações à lista
    
    return info_list


def validate_coords(place):
    '''Verifica se as coordenadas estão de acordo com o pedido na URL'''
    virgula_count = 0                                                       # variável para contar as virgulas inseridas
    valid = True                                                            # defenir o valor de valid como True

    for character in place:                                                 # iterar pelos caracteres do valor inserido pelo utilizador
        if character.isnumeric() or character == '-' or character == '.':  
            continue                                                        # ignorar caso os caracteres possam ser colocados no URI da API
        elif character == ',' and virgula_count < 1:
            virgula_count += 1                                              # caso se trate de uma virgula e ainda não se tenha colocado outra, continuar
            continue
        else:
            print('Formato das coordenadas incorreto!')                     # imprimir mensagem de erro   
            valid = False                                                   # tudo o resto deverá tranformar a variável "valid" em False
    
    if valid:                                                               # caso "valid" se mantenha True
        try:                                                                # tentar realizar as seguintes ações
            coords_list = place.replace(',', ' ').split()                   # colocar as duas coordenadas numa lista
            latitude, longitude = map(float, coords_list)                   # usamos "map" para tranformar todos os elementos da lista em float
            
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:          # garantir que as coordenadas estão nos limites definindos
                pass
            
            else:
                print('Coordenadas fora do intervalo permitido!')           # imprimir mensagem de erro 
                valid = False                                               # tornar a variavel "valid" em False
        
        except ValueError:                                                  # não possível possivel transformar as coordenadas em float por terem caracteres como "-" e "." a mais
            print('Formato das coordenadas incorreto!')                     # imprimir mensagem de erro
            valid = False                                                   # tornar a variável "valid" em False
    else:                                               
        pass
    
    return valid                                                            # return o valor de "valid"


def validate_categories(category):
    '''Verifica se as categorias estão de acordo com o pedido na URL'''
    valid = True                                                            # definir o valor de "valid" como True
    for character in category:                                              # iterar pelos caracteres das categorias inseridas pelo utilizador
        if character.isalpha() or character == ',' or character == '.':     # caso algum dos caracters for do tipo representado, continuar
            continue
        else:                                                               # se algum caracter n for do tipo acima, tornar "valid" em False
            print('Formato das categorias incorreto!')                      # imprimir mensagem de erro
            valid = False

    users_categories_list = category.replace(',', ' ').split()              # colocar as categorias numa lista separadas por virgulas

    if valid == False:                                                      # se "valid" for False, ignorar
        pass
    else:
        for categories in users_categories_list:                            # iterar pelas categorias da lista e verificar se estão no set criado pela função "set_of_categories"
            if categories not in set_of_categories():
                print('Formato das categorias incorreto!')                  # imprimir mensagem de erro
                valid = False                                               # tornar a variàvel "valid" False
                break                                                       # parar o loop do for
       
    return valid


def validate_radius(radius):
    '''Verifica se o raio estão de acordo com o pedido na URL'''
    not_num = 0                                                             # variável para contar os characters que não são números
    ponto_count = 0                                                         # variável para contar os caracteres que são pontos
    valid = True                                                            # defenir "valid" como True
    for num in radius:                                                      # iterar pelos caracteres do raio inserido pelo utilizador
        if num.isnumeric() or (num == '.' and ponto_count < 2):             # caso o caracter for um número ou um ponto e só se tenha utilizado um ponto
            continue        
        else:                                                               # tudo o resto, adiciona-se um à variável "not_num"
            not_num += 1
    
    if not_num == 0:                                                        # todos os caracteres dão números ou um ponto
        pass
    else:
        print('Valor para raio não suportado!')                             # imprimir mensagem de erro
        valid = False                                                       # dar o valor de False a "valid"
    
    return valid


def order_to(order, places_info):
    """Função para ordenar a informação segundo a preferência do utilizador"""
    info = []                                                               # lista onde será colocada a informação
    if order == '0':
        for dic in places_info:
            if 'distance' in dic.keys():
                info.append(dic)
        Info = sorted(places_info, key= lambda v: v['distance'])
        return Info
    elif order == "1":
        for dic in places_info:
            if 'categories' in dic.keys():
                info.append(dic)
        Info = sorted(places_info, key= lambda v: v['categories'])
        return Info
    elif order == "2":
        for dic in places_info:
            if 'name' in dic.keys():
                info.append(dic)
        Info = sorted(info, key= lambda v: v['name'])
        return Info


def print_info(info, category):
    count = 0
    distancia_total = 0
    if len(info) == 0:
        print('Nenhuma informação encontrada sobre o local!') 
    else:
        print("| {:^40s} | {:^40s} | {:^20s} | {:^20s} | {:^14s} | {:^15s} |".format("Tipo Atração", "Nome", "Local", "Coordenadas", "Distância [M]", "Fuso-horário"))
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
                distance = round(dic.get('distance', 0), 3)
                fuso_horario = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
                print(f"| {tipo_atração:^40s} | {name:^40s} | {local: ^20s} | {str(latitude) + ', ' + str(longitude):^20s} |  {distance:^13} | {fuso_horario:^15} |")
                count += 1
                distancia_total += distance
        
        print()
        print(f'Foram encontradas {count} atrações segundo as categorias indicadas!')
        print(f'A distância média às atrações é de {round(distancia_total / count)} m')

def info_extra(extra_info, places_info):
    if extra_info in ['S']:
        print('-' * 30)
        print('Aqui estão algumas informações extra:')
        print()
        for dic in places_info:
            if 'name' in dic.keys():
                print(f"{dic['name']}: País: {dic['country']} [{dic['country_code']}]; Distrito:{dic['county']}; endereço: {dic['address_line2']}")
                print('=' * 30)
                sleep(0.2)
        print('Obrigado pela preferência! Volte sempre!')
    elif extra_info in ['N']:
        print('Obrigado pela preferência! Volte sempre!')

        
                    
def main():
    '''função principal'''
    
    base_url = "https://api.geoapify.com/v2/places?"
    apiKey = '5151ac446fb14f58b87dda914081fd3d'
    
    coords = input('Place coordinates (lat,lon): ')
    category = input('Category to search for: ')
    radius = input('Circle radius: ')

    order_list = input('Order information by: [0]Distance, [1]Alphabetical order of category, [2]Alphabeticalorder of name --> R: ')
    while order_list not in "123":
        print('Resposta inválida!')
        order_list = input('Order information by: [0] distance, [1]Alphabetical order of category, [2]Alphabeticalorder of name\nR: ')

    if validate_coords(coords):
        coords_list = coords.split(',')
        coords1 = str(coords_list[0])
        coords2 = str(coords_list[1])
        coords_reverse = coords2 + ',' + coords1

    url = (f'{base_url}categories={category}&filter=circle:{coords_reverse},{radius}&bias=proximity:{coords_reverse}&limit=20&apiKey={apiKey}') if (validate_coords(coords) and validate_categories(category) and validate_radius(radius)) else main()
    
    places_info = get_info(url)
    places_info = order_to(order_list, places_info)
    
    print_info(places_info, category)

    extra_info = input('Deseja ver informação adicional sobre os locais que pesquisou? [S/N]: ').upper()
    while extra_info not in ['S', 'N']:
        print('Responda de acordo com a forma que é pedida!')
        extra_info = input('Deseja ver informação adicional sobre os locais que pesquisou? [S/N]: ').upper()
    info_extra(extra_info, places_info)

if __name__ == '__main__':
    main()
    
