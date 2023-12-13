import tkinter as tk
from tkinter import ttk
import requests
from requests.structures import CaseInsensitiveDict
from timezonefinder import TimezoneFinder
from time import sleep

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Consulta de Locais")

        self.label_coords = ttk.Label(master, text="Place coordinates (lat,lon):")
        self.entry_coords = ttk.Entry(master)

        self.label_category = ttk.Label(master, text="Category to search for:")
        self.entry_category = ttk.Entry(master)

        self.label_radius = ttk.Label(master, text="Circle radius:")
        self.entry_radius = ttk.Entry(master)

        self.label_order = ttk.Label(master, text="Order information by:")
        self.entry_order = ttk.Entry(master)

        self.button_search = ttk.Button(master, text="Search", command=self.search)

        self.label_result = ttk.Label(master, text="Results:")
        self.text_result = tk.Text(master, height=10, width=50)

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

        if self.validate_input(coords, category, radius, order_list):
            result = self.get_info(coords, category, radius, order_list)
            self.text_result.delete(1.0, tk.END)  # Clear previous results
            self.text_result.insert(tk.END, result)

    def validate_input(self, coords, category, radius, order_list):
        # TODO: Adicione sua lógica de validação aqui
        return True

    def get_info(self, coords, category, radius, order_list):
        # TODO: Adicione sua lógica para obter informações aqui
        return "Results will be displayed here."

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()