""""
Inventory Management System - Meijer
Author: Team 4
Description:
A Python-based inventory management system for Meijer.
This system allows store employees to track products, manage stock levels,
record sales, and generate reports. It includes a Tkinter-based GUI and
uses multiple collections (list, dict, tuple, array) to manage data.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import datetime
from array import array
import json

# --- Classes ---

class Product:
    """Represents a product with name, SKU, price, quantity, category"""
    def __init__(self, name, sku, price, quantity, category):
        self.name = name
        self.sku = sku
        self.price = price
        self.quantity = quantity
        self.category = category
        self.attributes = (self.sku, self.category)  # tuple usage

    def update_stock(self, amount):
        self.quantity += amount

    def to_dict(self):
        return {
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

    def __str__(self):
        return f"{self.sku}: {self.name} - ${self.price:.2f} ({self.quantity} in stock)"


class Inventory:
    """Manages products using a dictionary, list, and array"""
    def __init__(self):
        self.products_dict = {}
        self.products_list = []
        self.stock_array = array('i', [])

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

    def save_to_file(self, filename="inventory_data.json"):
        data = [p.to_dict() for p in self.products_list]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="inventory_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    product = Product(item["name"], item["sku"], item["price"],
                                      item["quantity"], item["category"])
                    self.add_product(product)
        except FileNotFoundError:
            pass  # No previous file, start fresh


class Sales:
    """Handles sales transactions and updates inventory"""
    def __init__(self):
        self.sales_log = []  # list of tuples (sku, qty, datetime)

    def record_sale(self, sku, quantity):
        self.sales_log.append((sku, quantity, datetime.datetime.now()))

    def generate_sales_report(self):
        return [f"Product {sku}, Quantity: {qty}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                for (sku, qty, time) in self.sales_log]


class Report:
    """Generates formatted reports for inventory and sales"""
    @staticmethod
    def generate_inventory_report(inventory):
        return "\n".join(inventory.list_products()) or "No products in inventory."

    @staticmethod
    def generate_sales_report(sales):
        return "\n".join(sales.generate_sales_report()) or "No sales recorded yet."


class GUI:
    """Tkinter GUI for interacting with the inventory system"""
    def __init__(self, inventory, sales):
        self.inventory = inventory
        self.sales = sales

        self.root = tk.Tk()
        self.root.title("Meijer Inventory Management System")
        self.root.geometry("400x350")

        tk.Label(self.root, text="Meijer Inventory Management", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.root, text="Show Inventory", command=self.show_inventory, width=25).pack(pady=3)
        tk.Button(self.root, text="Add Product", command=self.add_product, width=25).pack(pady=3)
        tk.Button(self.root, text="Remove Product", command=self.remove_product, width=25).pack(pady=3)
        tk.Button(self.root, text="Record Sale", command=self.record_sale, width=25).pack(pady=3)
        tk.Button(self.root, text="Show Sales Report", command=self.show_sales_report, width=25).pack(pady=3)
        tk.Button(self.root, text="Save Inventory", command=self.save_inventory, width=25).pack(pady=3)
        tk.Button(self.root, text="Exit", command=self.root.destroy, width=25, bg="red", fg="white").pack(pady=10)

        self.root.mainloop()

    def show_report_window(self, title, text):
        """Open a scrollable window to show reports"""
        win = tk.Toplevel(self.root)
        win.title(title)
        txt = scrolledtext.ScrolledText(win, width=60, height=20)
        txt.insert(tk.END, text)
        txt.config(state="disabled")
        txt.pack(padx=10, pady=10)

    def show_inventory(self):
        report = Report.generate_inventory_report(self.inventory)
        self.show_report_window("Inventory Report", report)

    def add_product(self):
        try:
            name = simpledialog.askstring("Input", "Product Name:")
            if not name: return
            sku = simpledialog.askstring("Input", "SKU:")
            if not sku: return
            price = float(simpledialog.askstring("Input", "Price:"))
            quantity = int(simpledialog.askstring("Input", "Quantity:"))
            category = simpledialog.askstring("Input", "Category:")
            if not category: category = "Uncategorized"

            product = Product(name, sku, price, quantity, category)
            self.inventory.add_product(product)
            messagebox.showinfo("Success", f"Product '{name}' added successfully.")
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def remove_product(self):
        sku = simpledialog.askstring("Input", "Enter SKU to remove:")
        if not sku: return
        product = self.inventory.get_product(sku)
        if product:
            self.inventory.remove_product(sku)
            messagebox.showinfo("Removed", f"Product '{product.name}' removed.")
        else:
            messagebox.showerror("Error", "SKU not found.")

    def record_sale(self):
        sku = simpledialog.askstring("Input", "SKU of product sold:")
        if not sku: return
        product = self.inventory.get_product(sku)
        if not product:
            messagebox.showerror("Error", "SKU not found.")
            return
        try:
            qty = int(simpledialog.askstring("Input", "Quantity sold:"))
            if qty <= 0:
                raise ValueError
            if qty > product.quantity:
                messagebox.showerror("Error", "Not enough stock.")
                return
            product.update_stock(-qty)
            index = self.inventory.products_list.index(product)
            self.inventory.stock_array[index] = product.quantity
            self.sales.record_sale(sku, qty)
            messagebox.showinfo("Sale Recorded", f"Sold {qty} of {product.name}.")
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Invalid quantity.")

    def show_sales_report(self):
        report = Report.generate_sales_report(self.sales)
        self.show_report_window("Sales Report", report)

    def save_inventory(self):
        self.inventory.save_to_file()
        messagebox.showinfo("Saved", "Inventory data saved successfully.")


# --- Main Program ---
def main():
    inventory = Inventory()
    inventory.load_from_file()
    sales = Sales()

    # Example products 
    if not inventory.products_list:
        inventory.add_product(Product("Apple", "SKU001", 0.99, 100, "Fruit"))
        inventory.add_product(Product("Milk", "SKU002", 2.49, 50, "Dairy"))
        inventory.add_product(Product("Bread", "SKU003", 1.99, 75, "Bakery"))

    GUI(inventory, sales)


if __name__ == "__main__":
    main()
