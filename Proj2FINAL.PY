from time import sleep
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder
from datetime import datetime
import os
import requests
import pytz
import sys

def set_of_categories():
    '''função que coloca as categorias de categories.txt num conjunto'''
    
    categories_set = set()                                              # criar um set vazio
    
    with open('categories.txt', 'r', encoding='utf-8') as file:         # abrir ficheiro "categories.txt"
        for line in file:                                               # iterar pelas linhas
            category = line.strip()                                     # remover tudo o que vier no final da linha
            categories_set.add(category)                                # adicionar categoria ao set
        
    return categories_set                                               # returnar set



def get_info(url):
    '''Informação útil acerca do local e categorias escolhidas pelo utilizador'''
    
    info_list = []                                      # lista onde será colocada a informação obtida pela API 
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(url, headers=headers)
    json_response = response.json()                     # colocar informação num dicionário
    all_info_list = (json_response.get('features'))     # selecionar apenas a informação relativa às 'features' do local
    
    for item in all_info_list:
        place_property_dict = item.get('properties')    # obter o valor das properties
        place_property_dict.pop('datasource')           # remover datasource
        place_property_dict.pop('place_id')             # remover place id 
        info_list.append(place_property_dict)           # adicionar dicionário com as informações à lista
    
    return info_list



def validate_coords(place):
    '''Verifica se as coordenadas estão de acordo com o pedido na URL'''
    virgula_count = 0                                                       # variável para contar as virgulas inseridas
    valid = True                                                            # defenir o valor de 'valid' como True

    for character in place:                                                 # iterar pelos caracteres das coordenadas inseridas pelo utilizador
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
                break                                                       # parar o for loop
       
    return valid



def validate_radius(radius):
    '''Verifica se o raio estão de acordo com o pedido na URL'''
    
    not_num = 0                                                             # variável para contar os caracteres que não são números
    ponto_count = 0                                                         # variável para contar os caracteres que são pontos
    valid = True                                                            # defenir "valid" como True
    
    for num in radius:                                                      # iterar pelos caracteres do raio inserido pelo utilizador
        if num.isnumeric() or (num == '.' and ponto_count < 2):             # caso o caracter for um número ou um ponto e só se tenha utilizado um ponto
            continue        
        else:                                                               # tudo o resto, adiciona-se uma unidade à variável "not_num"
            not_num += 1
    
    if not_num == 0:                                                        # todos os caracteres são números ou um ponto
        pass
    
    else:
        print('Valor para raio não suportado!')                             # imprimir mensagem de erro
        valid = False                                                       # dar o valor de False a "valid"
    
    return valid



def order_info(places_info):
    """Função para ordenar a informação segundo a preferência do utilizador"""
    
    info = []                                                                                   # lista onde será colocada a informação ordenada
    order_input = input('Order information by: \n[0]Distance\n[1]Category\n[2]Name\n[3]Location\nR: ')
    
    while order_input not in "0123":
        print('Resposta inválida!')
        order_input = input('Order information by: \n[0]Distance\n[1]Category\n[2]Name\n[3]Location\nR: ')
    
    if order_input == '0':
        for dic in places_info:
            if 'distance' in dic.keys():                                                        # ordenar informação por distancia
                info.append(dic)
        info_ordered = sorted(info, key= lambda v: v['distance'])
    
    elif order_input == "1":
        for dic in places_info:
            if 'categories' in dic.keys():                                                      # ordenar informação por categorias alfabeticamente
                info.append(dic)
        info_ordered = sorted(info, key= lambda v: v['categories'])
    
    elif order_input == "2":
        for dic in places_info:
            if 'name' in dic.keys():
                info.append(dic)                                                                # ordenar informação por nome alfabeticamente
        info_ordered = sorted(info, key= lambda v: v['name'])
    
    elif order_input == "3":
        for dic in places_info:
            if 'city' in dic.keys():
                info.append(dic)                                                                # ordenar informação por localização alfabeticamente
        info_ordered = sorted(info, key= lambda v: v['city'])
        
    return info_ordered



def obter_fuso_horario(latitude, longitude):
    '''Função para obter o fuso horário do local'''
    
    tf = TimezoneFinder()
    try:
        
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)                                          # Obtém o nome do fuso horário a partir das coordenadas

        if timezone_str:
            
            tz = pytz.timezone(timezone_str)                                                                # Obtém o objeto de fuso horário usando pytz
            
            
            offset_minutes = tz.utcoffset(datetime.now()).seconds // 60                                     # Obtém o offset atual do fuso horário em relação ao UTC em minutos

            
            offset_hours = offset_minutes // 60
            offset_minutes = offset_minutes % 60                                                            
            offset_str = f"{'' if offset_hours >= 0 else '-'}{abs(offset_hours):02d}:{offset_minutes:02d}"  # Converte o offset para o formato GMT

            tuplo_tz = (timezone_str + ':' + offset_str)

            return tuplo_tz
        else:
            return "Not Found"

    except Exception:
        return "Not Found"



def print_info(info, category, file=sys.stdout):
    '''Imprime a informação no terminal'''
   
    count = 0                                                                                                                                                                       # variável para contar o número de atrações
    distancia_total = 0                                                                                                                                                             # variável para guardar a distância total
    
    print("| {:^20s} | {:^40s} | {:^20s} | {:^20s} | {:^14s} | {:^19s} |".format("Tipo Atração", "Nome", "Local", "Coordenadas", "Distância [M]", "Fuso-horário"), file=file)       # imprime o título da tabela com as devidas formatações
    
    for dic in info:                                                                                                                                                                # iterar pelos dicionários na lista com as informações                                                                                                                                                     
        
        if dic.get('name', '') == '':                                                                                                                                               # caso a atração não tenha um nome, continuar
            continue
        
        else:
            users_categories_list = category.replace(',', ' ').split()                                                                                                              # colocar as categorias inseridas pleo utilizador numa lista
            tipo_atração = ''                                                                                                                                                       # variável inicial para tipo de atração
                
            for item in dic.get('categories'):                                                                                                                      
                
                if '.' in item:
                        continue        # iterar pelas categorias associadas do local e caso não tenha um '.' e estejam na lista de categorias introduzidas pelo utilizador, adicionar ao 'tipo_atracao'
                else:
                        tipo_atração += (item.capitalize() + ', ') if (item in users_categories_list) else ''
                
            if tipo_atração[-2] == ',':                                     # remover a ultima vírgula
                    tipo_atração = tipo_atração[:-2] + tipo_atração[-1]

            name = dic.get('name')                                  # obter nome
            latitude = round(dic.get('lat', 0), 2)                  # obter latitude
            longitude = round(dic.get('lon', 0), 2)                 # obter longitude
            local = dic.get('city', 'Not found')                    # obter local
            distance = round(dic.get('distance', 0), 3)             # obter distância
            fuso_horario = obter_fuso_horario(latitude, longitude)  # obter fuso horário
                
            print(f"| {tipo_atração:^20s} | {name:^40s} | {local: ^20s} | {str(latitude) + ', ' + str(longitude):^20s} |  {distance:^13} | {fuso_horario:^15} |", file=file)        # imprimir linha da tabela devidamente formatada
            count += 1                          # adicionar uma unidade a count
            distancia_total += distance         # adicionar a distancia da atração a 'distância total'
        
    print(file=file)
    print(f'Foram encontradas {count} atrações segundo as categorias indicadas!', file=file)        # imprimir o nº de locais encontrados
    print(f'A distância média às atrações é de {round(distancia_total / count)} m', file=file)      # imprimir a distância média



def print_info_extra(places_info, file=sys.stdout):
    '''Imprime informação extra se assim o utilizador desejar'''

    print(file=file)
    print('Aqui estão algumas informações extra:', file=file)       # imprimir mensagem de informações extra
    print(file=file)

    for dic in places_info:
        
        if 'name' in dic:
            print((f"{dic.get('name', 'Not Found')}:"), file=file)      # imprimir informação extra devidamente formatada
            print((f"\tPaís --> {dic.get('country', 'Not Found')}, {dic.get('country_code', 'Not Found')}; Distrito --> {dic.get('county', 'Not Found')}; Endereço --> {dic.get('address_line2', 'Not Found')}"), file=file)
            print(file=file)
            sleep(0.2)



def write_file(info, category, extra_info_input):
    '''Coloca as informações num ficheiro csv ordendas por distância'''
    
    with open('places.csv', 'w', encoding='utf-8') as f:
        print_info(info, category, f)       # escrever aquilo que é impresso no terminal no ficheiro .csv

        if extra_info_input == 'S':
            print_info_extra(info, f)       # caso o utilizador deseje, escrever informação extra no ficheiro .csv



def main():
    '''função principal'''
    
    base_url = "https://api.geoapify.com/v2/places?"            # URL base da API
    apiKey = '5151ac446fb14f58b87dda914081fd3d'                 # API Key
    
    coords = input('Place coordinates (lat,lon): ')             # pedir coordenadas
    category = input('Category to search for: ')                # pedir categorias
    radius = input('Circle radius: ')                           # pedir raio

    if validate_coords(coords):                                 # caso as coordenadas tenham sido validadas:
        coords_list = coords.split(',')                         # colocar coorenadas num lista
        coords1 = str(coords_list[0])                           
        coords2 = str(coords_list[1])
        coords_reverse = coords2 + ',' + coords1                # alterar a ordem das coordendas para cumprir com o que é pedido na URL da API 

    
    url = (f'{base_url}categories={category}&filter=circle:{coords_reverse},{radius}&bias=proximity:{coords_reverse}&limit=500&apiKey={apiKey}') if (validate_coords(coords) and validate_categories(category) and validate_radius(radius)) else main()  # construir URL para pesquisa caso os parametros tenham sido validados corretamente de acordo com as funções
    
    places_info = get_info(url)                                                 # atribuir a places_info a lista que é returnada pela função 'get_info'
    
    if len(places_info) == 0:
                                                                                # se não existeram informações na API imprimir mensagem a informar
        print('Não foi encontrada informação acerca do local pedido!')
    
    else:
        
        ordered_places_info = order_info(places_info)                           # ordenar informação como o utilizador desejar
        
        print_info(ordered_places_info, category)                               # imprimir informação no terminal
        
        extra_info_input = input('Deseja ver informação adicional sobre os locais que pesquisou? [S/N]: ').upper()

        while extra_info_input not in 'SN':                                     # perguntar ao utilizador se pretende receber informação extra acerca do local
            print('Responda de acordo com a forma que é pedida!')
            extra_info_input = input('Deseja ver informação adicional sobre os locais que pesquisou? [S/N]: ').upper()
        
        if extra_info_input == 'S':
            print_info_extra(ordered_places_info)                               # imprimir informação extra, se for o caso
        
        csv = input('Deseja exporta a informação para um ficheiro de texto .csv? [S/N]: ').upper()   # perguntar ao utilizador se pretende exportar as informações fornecidas
        while csv not in 'SN':
            print('Responda de acordo com a forma que é pedida!')
            csv = input('Deseja exporta a informação para um ficheiro de texto .csv? [S/N]: ').upper()

        if csv == 'S':
            print('Criando ficheiro .csv das informações...')
            write_file(ordered_places_info, category, extra_info_input)             # escrever ficheiro .csv
            print('Ficheiro csv criado!')
    
    mais_places = input('Deseja obter mais informações sobre outros locais ou categorias? [S/N]').upper()
    
    
    while mais_places not in 'SN':
                                                                                                # ver se o utlizador pretende procurar por mais alguma atração
        print('Resposta inválida!')
        mais_places = input('Deseja obter mais informações sobre outros locais ou categorias? [S/N]').upper()

    
    if mais_places == 'S':
        print('Reiniciando...')
        sleep(1.5)
        if os.name == 'nt':                                     #verificar se o sistema operativo é windows
            os.system('cls')                                    #Limpar o ecrã
        else:                                                   #se não for windows
            os.system('clear')                                  #limpa o ecrã linux
        main()                                                  # repetir o programa
    
    else:
        print('Obrigado pela preferência! Volte sempre!')
        sleep(2)
        if os.name == 'nt':            
            os.system('cls')          
        else:                          
            os.system('clear')         
        quit()

if __name__ == '__main__':
    main()
    