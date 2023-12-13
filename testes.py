import requests
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder
import tkinter as tk
from tkinter import ttk
from time import sleep

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
    # ... (código não alterado)

def validate_categories(category):
    '''Verifica se as categorias estão de acordo com o pedido na URL'''
    # ... (código não alterado)

def validate_radius(radius):
    '''Verifica se o raio estão de acordo com o pedido na URL'''
    # ... (código não alterado)

def order_to(order, places_info):
    info = []
    if order == '0':
        # ... (código não alterado)
    elif order == "1":
        # ... (código não alterado)
    elif order == "2":
        # ... (código não alterado)

def print_info(info, category):
    # ... (código não alterado)

def info_extra(extra_info, places_info):
    # ... (código não alterado)

def main(coords, category, radius, order_list):
    '''função principal'''
    base_url = "https://api.geoapify.com/v2/places?"
    apiKey = '5151ac446fb14f58b87dda914081fd3d'

    if validate_coords(coords) and validate_categories(category) and validate_radius(radius):
        coords_list = coords.split(',')
        coords1 = str(coords_list[0])
        coords2 = str(coords_list[1])
        coords_reverse = coords2 + ',' + coords1

        url = f'{base_url}categories={category}&filter=circle:{coords_reverse},{radius}&bias=proximity:{coords_reverse}&limit=20&apiKey={apiKey}'
        places_info = get_info(url)
        places_info = order_to(order_list, places_info)

        info_str = ""
        for dic in places_info:
            # ... (código não alterado)
            info_str += f"{tipo_atração:^40s} | {name:^40s} | {local: ^20s} | {str(latitude) + ', ' + str(longitude):^20s} |  {distance:^13} | {fuso_horario:^15} |\n"

        return info_str

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

        self.label_result = ttk.Label(root, text="Results:")
        self.text_result = tk.Text(root, height=10, width=50)

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

        self.label_result.grid(row=5, column=0, sticky="e")
        self.text_result.grid(row=5, column=1, columnspan=2)

    def search(self):
        coords = self.entry_coords.get()
        category = self.entry_category.get()
        radius = self.entry_radius.get()
        order_list = self.entry_order.get()

        result = main(coords, category, radius, order_list)
        self.text_result.delete(1.0, tk.END)
        self.text_result.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTkinterApp(root)
    root.mainloop()