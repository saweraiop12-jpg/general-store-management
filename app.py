

import tkinter as tk
from tkinter import ttk, messagebox

# Product Database (temporary)
products = {
    "Sugar": {"price": 160, "stock": 100},
    "Rice": {"price": 300, "stock": 50},
    "Milk": {"price": 220, "stock": 40},
    "Tea": {"price": 250, "stock": 60}
}

cart = []


# MAIN WINDOW
root = tk.Tk()
root.title("General Store Management System")
root.geometry("1000x650")
root.configure(bg="#eef2f7")


# HEADER
header = tk.Frame(root, bg="#183153", height=75)
header.pack(fill="x")

tk.Label(
    header,
    text="GENERAL STORE MANAGEMENT SYSTEM",
    font=("Arial", 21, "bold"),
    bg="#183153",
    fg="white"
).pack(pady=20)


# MAIN CONTENT
main_frame = tk.Frame(root, bg="#eef2f7")
main_frame.pack(fill="both", expand=True, padx=15, pady=15)


# LEFT MENU
menu = tk.Frame(main_frame, bg="#183153", width=190)
menu.pack(side="left", fill="y", padx=(0, 15))
menu.pack_propagate(False)


# RIGHT CONTENT
content = tk.Frame(main_frame, bg="white")
content.pack(side="right", fill="both", expand=True)


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


# DASHBOARD
def dashboard():

    clear_content()

    tk.Label(
        content,
        text="Welcome to Your Shop!",
        font=("Arial", 23, "bold"),
        bg="white"
    ).pack(pady=30)

    tk.Label(
        content,
        text="Manage products, stock and customer bills.",
        font=("Arial", 13),
        bg="white"
    ).pack(pady=10)

    info = tk.Frame(content, bg="white")
    info.pack(pady=40)

    tk.Label(
        info,
        text=f"Total Products: {len(products)}",
        font=("Arial", 17, "bold"),
        bg="#dbeafe",
        width=22,
        height=4
    ).grid(row=0, column=0, padx=15)

    tk.Label(
        info,
        text="Billing System\nReady",
        font=("Arial", 17, "bold"),
        bg="#dcfce7",
        width=22,
        height=4
    ).grid(row=0, column=1, padx=15)


# PRODUCT MANAGEMENT
def product_page():

    clear_content()

    tk.Label(
        content,
        text="PRODUCT MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=15)

    form = tk.Frame(content, bg="white")
    form.pack(pady=10)

    tk.Label(form, text="Product Name:", bg="white").grid(row=0, column=0)
    name_entry = tk.Entry(form, width=18)
    name_entry.grid(row=0, column=1, padx=10)

    tk.Label(form, text="Price:", bg="white").grid(row=0, column=2)
    price_entry = tk.Entry(form, width=12)
    price_entry.grid(row=0, column=3, padx=10)

    tk.Label(form, text="Stock:", bg="white").grid(row=0, column=4)
    stock_entry = tk.Entry(form, width=10)
    stock_entry.grid(row=0, column=5, padx=10)

    columns = ("Name", "Price", "Stock")

    tree = ttk.Treeview(
        content,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh():

        for row in tree.get_children():
            tree.delete(row)

        for name, data in products.items():
            tree.insert(
                "",
                "end",
                values=(name, data["price"], data["stock"])
            )

    def add_product():

        name = name_entry.get().strip()

        try:
            price = float(price_entry.get())
            stock = int(stock_entry.get())

            if not name or name in products:
                raise ValueError

            if price < 0 or stock < 0:
                raise ValueError

            products[name] = {
                "price": price,
                "stock": stock
            }

            refresh()

            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Product added!")

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a new product name, valid price and stock."
            )

    tk.Button(
        form,
        text="Add Product",
        bg="#2563eb",
        fg="white",
        command=add_product
    ).grid(row=1, column=2, pady=15)

    refresh()


# BILLING SYSTEM
def billing_page():

    clear_content()
    cart.clear()

    tk.Label(
        content,
        text="CUSTOMER BILLING",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=15)

    form = tk.Frame(content, bg="white")
    form.pack(pady=10)

    tk.Label(form, text="Select Product:", bg="white").grid(row=0, column=0)

    product_combo = ttk.Combobox(
        form,
        values=list(products.keys()),
        state="readonly",
        width=20
    )
    product_combo.grid(row=0, column=1, padx=10)

    tk.Label(form, text="Quantity:", bg="white").grid(row=0, column=2)

    qty_entry = tk.Entry(form, width=10)
    qty_entry.grid(row=0, column=3, padx=10)

    columns = ("Product", "Quantity", "Price", "Total")

    tree = ttk.Treeview(
        content,
        columns=columns,
        show="headings",
        height=11
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=20, pady=15)

    total_label = tk.Label(
        content,
        text="Grand Total: Rs. 0",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#15803d"
    )
    total_label.pack(pady=10)

    def add_to_cart():

        name = product_combo.get()

        try:
            qty = int(qty_entry.get())

            if not name or qty <= 0:
                raise ValueError

            if qty > products[name]["stock"]:
                messagebox.showerror(
                    "Stock Error",
                    "Not enough stock available!"
                )
                return

            price = products[name]["price"]

            existing = next(
                (item for item in cart if item["name"] == name),
                None
            )

            already_added = existing["qty"] if existing else 0

            if qty + already_added > products[name]["stock"]:
                messagebox.showerror(
                    "Stock Error",
                    "Not enough stock available!"
                )
                return

            if existing:
                existing["qty"] += qty
            else:
                cart.append({
                    "name": name,
                    "qty": qty,
                    "price": price
                })

            refresh_cart()
            qty_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Select a product and enter a valid quantity."
            )

    def refresh_cart():

        for row in tree.get_children():
            tree.delete(row)

        total = 0

        for item in cart:

            subtotal = item["qty"] * item["price"]
            total += subtotal

            tree.insert(
                "",
                "end",
                values=(
                    item["name"],
                    item["qty"],
                    item["price"],
                    subtotal
                )
            )

        total_label.config(
            text=f"Grand Total: Rs. {total:.2f}"
        )

    def complete_bill():

        if not cart:
            messagebox.showwarning(
                "Warning", "Cart is empty!"
            )
            return

        total = sum(
            item["qty"] * item["price"]
            for item in cart
        )

        for item in cart:
            products[item["name"]]["stock"] -= item["qty"]

        bill = "\n".join(
            f"{item['name']} x {item['qty']} = "
            f"Rs. {item['qty'] * item['price']}"
            for item in cart
        )

        messagebox.showinfo(
            "Customer Bill",
            f"GENERAL STORE\n\n"
            f"{bill}\n\n"
            f"Grand Total: Rs. {total:.2f}\n\n"
            f"Thank you for shopping!"
        )

        cart.clear()
        refresh_cart()

    buttons = tk.Frame(content, bg="white")
    buttons.pack(pady=10)

    tk.Button(
        buttons,
        text="Add to Bill",
        bg="#2563eb",
        fg="white",
        width=15,
        command=add_to_cart
    ).pack(side="left", padx=10)

    tk.Button(
        buttons,
        text="Complete Bill",
        bg="#15803d",
        fg="white",
        width=15,
        command=complete_bill
    ).pack(side="left", padx=10)


# STOCK MANAGEMENT
def stock_page():

    clear_content()

    tk.Label(
        content,
        text="STOCK MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=20)

    tree = ttk.Treeview(
        content,
        columns=("Product", "Available Stock"),
        show="headings"
    )

    tree.heading("Product", text="Product")
    tree.heading("Available Stock", text="Available Stock")

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    for name, data in products.items():
        tree.insert(
            "",
            "end",
            values=(name, data["stock"])
        )


# MENU BUTTONS
tk.Label(
    menu,
    text="MAIN MENU",
    font=("Arial", 16, "bold"),
    bg="#183153",
    fg="white"
).pack(pady=25)

buttons = [
    ("Dashboard", dashboard),
    ("Products", product_page),
    ("Billing", billing_page),
    ("Stock", stock_page)
]

for text, command in buttons:

    tk.Button(
        menu,
        text=text,
        font=("Arial", 12),
        bg="#27496d",
        fg="white",
        activebackground="#3b82f6",
        width=18,
        height=2,
        relief="flat",
        command=command
    ).pack(pady=8, padx=10)


tk.Button(
    menu,
    text="Exit",
    font=("Arial", 12, "bold"),
    bg="#dc2626",
    fg="white",
    width=18,
    height=2,
    command=root.destroy
).pack(side="bottom", pady=25)


# START APPLICATION
dashboard()

root.mainloop()
