"""
Inventory Management System - Meijer
Author: Team 4
Description: Our team proposes to build a Python-based inventory management system for Meijer. 
The system will allow store employees to track products, manage stock levels, and generate reports on inventory and sales.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from array import array

# --- Classes ---

class Product:
    """Represents a product with name, SKU, price, quantity, category"""
    def __init__(self, name, sku, price, quantity, category):
        self.name = name
        self.sku = sku
        self.price = price
        self.quantity = quantity
        self.category = category  # tuple usage
        self.attributes = (self.sku, self.category)

    def update_stock(self, amount):
        self.quantity += amount

    def __str__(self):
        return f"{self.sku}: {self.name} - ${self.price} ({self.quantity} in stock)"

class Inventory:
    """Manages products using a dictionary and a list"""
    def __init__(self):
        self.products_dict = {}
        self.products_list = []
        self.stock_array = array('i', [])  # Track quantities as array

    def add_product(self, product):
        self.products_dict[product.sku] = product
        self.products_list.append(product)
        self.stock_array.append(product.quantity)

    def remove_product(self, sku):
        product = self.products_dict.pop(sku, None)
        if product:
            index = self.products_list.index(product)
            self.products_list.pop(index)
            self.stock_array.pop(index)

    def get_product(self, sku):
        return self.products_dict.get(sku)

    def list_products(self):
        return [str(prod) for prod in self.products_list]

class Sales:
    """Handles sales transactions and updates inventory"""
    def __init__(self):
        self.sales_log = []  # List of tuples: (SKU, quantity, datetime)

    def record_sale(self, sku, quantity):
        self.sales_log.append((sku, quantity, datetime.datetime.now()))

    def generate_sales_report(self):
        return [f"Product {sku}, Quantity: {qty}, Time: {time}" 
                for (sku, qty, time) in self.sales_log]

class Report:
    """Generates formatted reports for inventory and sales"""
    @staticmethod
    def generate_inventory_report(inventory):
        return "\n".join(inventory.list_products())

    @staticmethod
    def generate_sales_report(sales):
        return "\n".join(sales.generate_sales_report())

class GUI:
    """Handles graphical interface and interactions"""
    def __init__(self, inventory, sales):
        self.inventory = inventory
        self.sales = sales

        self.root = tk.Tk()
        self.root.title("Meijer Inventory Management System")

        # GUI Elements
        tk.Label(self.root, text="Inventory Management System").pack()

        tk.Button(self.root, text="Show Inventory", command=self.show_inventory).pack()
        tk.Button(self.root, text="Add Product", command=self.add_product).pack()
        tk.Button(self.root, text="Remove Product", command=self.remove_product).pack()
        tk.Button(self.root, text="Record Sale", command=self.record_sale).pack()
        tk.Button(self.root, text="Show Sales Report", command=self.show_sales_report).pack()

        self.root.mainloop()

    def show_inventory(self):
        report = Report.generate_inventory_report(self.inventory)
        messagebox.showinfo("Inventory", report)

    def add_product(self):
        name = simpledialog.askstring("Input", "Product Name:")
        sku = simpledialog.askstring("Input", "SKU:")
        price = float(simpledialog.askstring("Input", "Price:"))
        quantity = int(simpledialog.askstring("Input", "Quantity:"))
        category = simpledialog.askstring("Input", "Category:")
        product = Product(name, sku, price, quantity, category)
        self.inventory.add_product(product)
        messagebox.showinfo("Success", f"Product {name} added.")

    def remove_product(self):
        sku = simpledialog.askstring("Input", "SKU of product to remove:")
        product = self.inventory.get_product(sku)
        if product:
            self.inventory.remove_product(sku)
            messagebox.showinfo("Success", f"Product {product.name} removed.")
        else:
            messagebox.showerror("Error", "SKU not found.")

    def record_sale(self):
        sku = simpledialog.askstring("Input", "SKU of product sold:")
        product = self.inventory.get_product(sku)
        if not product:
            messagebox.showerror("Error", "SKU not found.")
            return
        qty = int(simpledialog.askstring("Input", "Quantity sold:"))
        if qty > product.quantity:
            messagebox.showerror("Error", "Not enough stock.")
            return
        product.update_stock(-qty)
        index = self.inventory.products_list.index(product)
        self.inventory.stock_array[index] = product.quantity
        self.sales.record_sale(sku, qty)
        messagebox.showinfo("Success", f"Recorded sale of {qty} {product.name}(s).")

    def show_sales_report(self):
        report = Report.generate_sales_report(self.sales)
        if report:
            messagebox.showinfo("Sales Report", report)
        else:
            messagebox.showinfo("Sales Report", "No sales recorded yet.")

# --- Main Program ---
def main():
    inventory = Inventory()
    sales = Sales()

    # Add products
    inventory.add_product(Product("Apple", "SKU001", 0.99, 100, "Fruit"))
    inventory.add_product(Product("Milk", "SKU002", 2.49, 50, "Dairy"))
    inventory.add_product(Product("Bread", "SKU003", 1.99, 75, "Bakery"))

    gui = GUI(inventory, sales)

if __name__ == "__main__":
    main()

