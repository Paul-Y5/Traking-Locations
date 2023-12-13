import requests
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder
import tkinter as tk
from tkinter import ttk
from time import sleep

class SimpleTkinterApp:
    def __init__(self, root):
        self.root = root
        root.title("Consulta de Locais")

        self.label_coords = ttk.Label(root, text="Place coordinates (lat,lon):")
        self.entry_coords = ttk.Entry(root)

        self.label_category = ttk.Label(root, text="Category to search for:")
        self.entry_category = ttk.Entry(root)

        self.label_radius = ttk.Label(root, text="Circle radius:")
        self.entry_radius = ttk.Entry(root)

        self.label_order = ttk.Label(root, text="Order information by:")
        self.entry_order = ttk.Entry(root)

        self.button_search = ttk.Button(root, text="Search", command=self.search)

        # Create a Treeview widget for displaying results
        self.tree = ttk.Treeview(root, columns=("Tipo Atração", "Nome", "Local", "Coordenadas", "Distância [M]", "Fuso-horário"))

        # Define column headings
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("Tipo Atração", text="Tipo Atração")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Local", text="Local")
        self.tree.heading("Coordenadas", text="Coordenadas")
        self.tree.heading("Distância [M]", text="Distância [M]")
        self.tree.heading("Fuso-horário", text="Fuso-horário")

        # Define column widths
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Tipo Atração", anchor="w", width=150)
        self.tree.column("Nome", anchor="w", width=250)
        self.tree.column("Local", anchor="w", width=150)
        self.tree.column("Coordenadas", anchor="w", width=150)
        self.tree.column("Distância [M]", anchor="w", width=100)
        self.tree.column("Fuso-horário", anchor="w", width=150)

        # Grid layout
        self.label_coords.grid(row=0, column=0, sticky="e")
        self.entry_coords.grid(row=0, column=1)

        self.label_category.grid(row=1, column=0, sticky="e")
        self.entry_category.grid(row=1, column=1)

        self.label_radius.grid(row=2, column=0, sticky="e")
        self.entry_radius.grid(row=2, column=1)

        self.label_order.grid(row=3, column=0, sticky="e")
        self.entry_order.grid(row=3, column=1)

        self.button_search.grid(row=4, column=0, columnspan=2)

        self.tree.grid(row=5, column=0, columnspan=2)

    def set_of_categories(self):
        '''função que coloca as categorias de categories.txt num conjunto'''
        categories_set = set()
        with open('categories.txt', 'r', encoding='utf-8') as file:
            for line in file:
                category = line.strip()
                categories_set.add(category)
        return categories_set

    def get_info(self, url):
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

    def validate_coords(self, place):
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
                self.text_result.delete(1.0, tk.END)
                self.text_result.insert(tk.END, 'Formato das coordenadas incorreto!')
                valid = False

        if valid:
            try:
                coords_list = place.replace(',', ' ').split()
                latitude, longitude = map(float, coords_list)

                if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                    pass
                else:
                    self.text_result.delete(1.0, tk.END)
                    self.text_result.insert(tk.END, 'Coordenadas fora do intervalo permitido!')
                    valid = False

            except ValueError:
                self.text_result.delete(1.0, tk.END)
                self.text_result.insert(tk.END, 'Formato das coordenadas incorreto!')
                valid = False

        return valid

    def validate_categories(self, category):
        '''Verifica se as categorias estão de acordo com o pedido na URL'''
        valid = True
        for character in category:
            if character.isalpha() or character == ',' or character == '.':
                continue
            else:
                self.text_result.delete(1.0, tk.END)
                self.text_result.insert(tk.END, 'Formato das categorias incorreto!')
                valid = False

        users_categories_list = category.replace(',', ' ').split()

        if valid == False:
            pass
        else:
            for categories in users_categories_list:
                if categories not in self.set_of_categories():
                    self.text_result.delete(1.0, tk.END)
                    self.text_result.insert(tk.END, 'Formato das categorias incorreto!')
                    valid = False
                    break

        return valid

    def validate_radius(self, radius):
        '''Verifica se o raio estão de acordo com o pedido na URL'''
        not_num = 0
        ponto_count = 0
        valid = True
        for num in radius:
            if num.isnumeric() or (num == '.' and ponto_count < 2):
                continue
            else:
                self.text_result.delete(1.0, tk.END)
                self.text_result.insert(tk.END, 'Valor para raio não suportado!')
                valid = False

        return valid

    def order_info(self, places_info):
        """Função para ordenar a informação segundo a preferência do utilizador"""
        info = []
        order_input = self.entry_order.get()

        while order_input not in "012":
            self.text_result.delete(1.0, tk.END)
            self.text_result.insert(tk.END, 'Resposta inválida!')
            order_input = self.entry_order.get()

        if order_input == '0':
            for dic in places_info:
                if 'distance' in dic.keys():
                    info.append(dic)
            info_ordered = sorted(places_info, key=lambda v: v['distance'])

        elif order_input == "1":
            for dic in places_info:
                if 'categories' in dic.keys():
                    info.append(dic)
            info_ordered = sorted(places_info, key=lambda v: v['categories'])

        elif order_input == "2":
            for dic in places_info:
                if 'name' in dic.keys():
                    info.append(dic)
            info_ordered = sorted(info, key=lambda v: v['name'])

        return info_ordered

    def print_info(self, info, category):
        count = 0
        distancia_total = 0

        result_text = "| {:^20s} | {:^40s} | {:^20s} | {:^20s} | {:^14s} | {:^15s} |\n".format(
            "Tipo Atração", "Nome", "Local", "Coordenadas", "Distância [M]", "Fuso-horário")

        for dic in info:
            if dic.get('name', '') == '':
                continue
            else:
                users_categories_list = category.replace(',', ' ').split()
                tipo_atracao = ''

                for item in dic.get('categories'):
                    if '.' in item:
                        continue
                    else:
                        tipo_atracao += (item.capitalize() + ', ') if (item in users_categories_list) else ''

                if tipo_atracao[-2] == ',':
                    tipo_atracao = tipo_atracao[:-2] + tipo_atracao[-1]

                name = dic.get('name')
                latitude = round(dic.get('lat', 0), 2)
                longitude = round(dic.get('lon', 0), 2)
                local = dic.get('city', 'Not found')
                distance = round(dic.get('distance', 0), 3)
                fuso_horario = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)

                result_text += "| {:^20s} | {:^40s} | {:^20s} | {:^20s} |  {:^13} | {:^15} |\n".format(
                    tipo_atracao, name, local, str(latitude) + ', ' + str(longitude), distance, fuso_horario)

                count += 1
                distancia_total += distance

        result_text += '\n'
        result_text += f'Foram encontradas {count} atrações segundo as categorias indicadas!\n'
        result_text += f'A distância média às atrações é de {round(distancia_total / count)} m'

        self.text_result.delete(1.0, tk.END)
        self.text_result.insert(tk.END, result_text)

    def build_url(self, coords, category, radius):
        base_url = "https://api.geoapify.com/v2/places?"
        api_key = '5151ac446fb14f58b87dda914081fd3d'

        coords_list = coords.split(',')
        coords1 = str(coords_list[0])
        coords2 = str(coords_list[1])
        coords_reverse = coords2 + ',' + coords1

        url = f"{base_url}categories={category}&filter=circle:{coords_reverse},{radius}&bias=proximity:{coords_reverse}&limit=20&apiKey={api_key}"
        return url

    def search(self):
        coords = self.entry_coords.get()
        category = self.entry_category.get()
        radius = self.entry_radius.get()

        if self.validate_coords(coords) and self.validate_categories(category) and self.validate_radius(radius):
            url = self.build_url(coords, category, radius)

            # Obtenha informações e ordene, conforme necessário
            places_info = self.get_info(url)
            ordered_places_info = self.order_info(places_info)

            # Exiba as informações na interface gráfica
            self.print_info(ordered_places_info, category)
        else:
            # Exiba uma mensagem de erro na interface gráfica
            self.text_result.delete(1.0, tk.END)
            self.text_result.insert(tk.END, "Dados de entrada inválidos. Verifique e tente novamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTkinterApp(root)
    root.mainloop()
