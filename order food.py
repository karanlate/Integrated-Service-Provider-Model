import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import asyncio
import winsdk.windows.devices.geolocation as wdg

restaurants = {
    "Restaurant 1": {
        "menu": {
            "Pizza": 10,
            "Burger": 8,
            "Pasta": 12,
        }
    },
    "Restaurant 2": {
        "menu": {
            "Steak": 15,
            "Salad": 7,
            "Soup": 6,
        }
    },
    # Add more restaurants and their menus here
}

def add_to_cart():
    selected_item = menu_listbox.get(tk.ACTIVE)
    quantity = quantity_var.get()

    if selected_item and quantity > 0:
        if selected_item in cart:
            cart[selected_item] += quantity
        else:
            cart[selected_item] = quantity

        cart_listbox.delete(0, tk.END)
        for item, qty in cart.items():
            cart_listbox.insert(tk.END, f"{item} x {qty}")

        messagebox.showinfo("Cart Updated", f"{quantity} {selected_item}(s) added to the cart.")
    else:
        messagebox.showerror("Error", "Please select an item and specify a valid quantity.")

def remove_from_cart():
    selected_item = cart_listbox.get(tk.ACTIVE)
    if selected_item:
        item, qty = selected_item.split(" x ")
        cart[item] -= int(qty)
        if cart[item] <= 0:
            del cart[item]

        cart_listbox.delete(tk.ACTIVE)
        messagebox.showinfo("Cart Updated", f"{qty} {item}(s) removed from the cart.")
    else:
        messagebox.showerror("Error", "Please select an item to remove.")

def place_order():
    if cart:
        messagebox.showinfo("Order Confirmation", "Your order has been placed successfully!")
        order_message = get_order()  # Get the items in the cart as a string
        cart.clear()
        cart_listbox.delete(0, tk.END)
        messagebox.showinfo("Order Details", order_message)  # Display the order details
    else:
        messagebox.showerror("Error", "Your cart is empty. Please add items to place an order.")

def get_order():
    order_message = "Order List:\n"
    for item, qty in cart.items():
        order_message += f"{qty} x {item}\n"
    return order_message

def final_order():
    order_message = "Order List:\n"
    for item, qty in cart.items():
        order_message += f"{qty} x {item}\n"
    return order_message


def update_menu(*args):
    selected_restaurant = restaurant_var.get()
    menu_listbox.delete(0, tk.END)
    if selected_restaurant in restaurants:
        menu = restaurants[selected_restaurant]["menu"]
        for item, price in menu.items():
            menu_listbox.insert(tk.END, f"{item} - ${price}")

# Set up Twilio client
account_sid = "AC8a5f78a4e5b768e7aa290a4da402d1d8"
auth_token = "ee80b119deafeb13cb831d98180b1f98"
client = Client(account_sid, auth_token)

# Get location from a GPS-enabled device
async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]


def getLoc():
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        print("ERROR: You need to allow applications to access you location in Windows settings")

def sendLocationSMS():
    text1 = phone.get()
    text2 = final_order
    if text1:
        cord = getLoc()
        lat = cord[0]
        lon = cord[1]
        message = "My current location is: https://www.google.com/maps/search/?api=1&query=" + str(lat) + "," + str(
            lon) + "\n" + "Customer Contact Number :" + str(text1) + "\n" + str(text2)
        to_number = "+917397805884"
        from_number = "+15855846197"
        client.messages.create(
            to=to_number,
            from_=from_number,
            body=message)
        success_label.config(text="SMS sent successfully!")
    else:
        success_label.config(text="Please enter some text.")

# Create label for success message
success_label = tk.Label(text="")
success_label.pack()

def button_command():
    place_order()
    sendLocationSMS()


def show(root):
    # Create the option page widgets
    label = tk.Label(root)
    label.pack()
    global phone
    phone = tk.Entry(width=30, font=("TkDefaultFont", 9))
    # add a placeholder text
    phone.insert(0, "Enter Contact Number Here...")

    def on_phone_click(event):
        if phone.get() == "Enter Contact Number Here...":
            phone.delete(0, "end")  # delete all the text in the entry
            phone.insert(0, "")  # insert blank for user input

    # bind the on_entry_click function to the entry widget
    phone.bind("<FocusIn>", on_phone_click)
    phone.pack()

    global restaurant_var
    restaurant_label = tk.Label(root, text="Select Restaurant:")
    restaurant_label.pack()

    restaurant_var = tk.StringVar()
    restaurant_dropdown = tk.OptionMenu(root, restaurant_var, *restaurants.keys())
    restaurant_dropdown.pack()

    menu_label = tk.Label(root, text="Menu:")
    menu_label.pack()

    global menu_listbox
    menu_listbox = tk.Listbox(root,height=7)
    menu_listbox.pack()

    quantity_label = tk.Label(root, text="Quantity:")
    quantity_label.pack()

    global quantity_var
    quantity_var = tk.IntVar()
    quantity_entry = tk.Entry(root, textvariable=quantity_var)
    quantity_entry.pack()

    cart_label = tk.Label(root, text="Cart:")
    cart_label.pack()

    global cart_listbox
    cart_listbox = tk.Listbox(root,height=7)
    cart_listbox.pack()

    button_frame = tk.Frame(root)
    button_frame.pack()

    add_button = tk.Button(button_frame, text="+ Add to Cart", command=add_to_cart)
    add_button.pack(side=tk.LEFT)

    remove_button = tk.Button(button_frame, text="- Remove from Cart", command=remove_from_cart)
    remove_button.pack(side=tk.LEFT)

    order_button = tk.Button(root, text="Place Order", command=button_command)
    order_button.pack()

    restaurant_var.trace("w", update_menu)

    global cart
    cart = {}

