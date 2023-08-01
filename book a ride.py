import tkinter as tk
from twilio.rest import Client
import asyncio
import winsdk.windows.devices.geolocation as wdg
import folium
from geopy.geocoders import Nominatim
import webbrowser
from math import sin, cos, sqrt, atan2, radians

def show(root):
    # Create the option page widgets
    label = tk.Label(root)
    label.pack(pady=20)

# Create input label
label_font = ("TkDefaultFont", 15)
input_label = tk.Label(text="Your Current Location",font=label_font)
input_label.pack(pady=10)
phone=tk.Entry(width=30, font=("TkDefaultFont", 12))
# add a placeholder text
phone.insert(0, "Enter Contact Number Here...")
def on_phone_click(event):
    if phone.get() == "Enter Contact Number Here...":
        phone.delete(0, "end")  # delete all the text in the entry
        phone.insert(0, "")  # insert blank for user input
# bind the on_entry_click function to the entry widget
phone.bind("<FocusIn>", on_phone_click)
phone.pack()
add=tk.Entry(width=100, font=("TkDefaultFont", 12))
# add a placeholder text
add.insert(0, "Enter Your Desire Destination")
def on_add_click(event):
    if add.get() == "Enter Your Desire Destination":
        add.delete(0, "end")  # delete all the text in the entry
        add.insert(0, "")  # insert blank for user input
# bind the on_entry_click function to the entry widget
add.bind("<FocusIn>", on_add_click)
add.pack()

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
    text2 = add.get()
    if text1 and text2 :
        cord = getLoc()
        lat = cord[0]
        lon = cord[1]
        message = "My current location is: https://www.google.com/maps/search/?api=1&query=" + str(lat) + "," + str(
            lon) + "\n" + "Customer Contact Number :" + str(text1) + "\n" + "Address :" + str(text2)
        to_number = "+917397805884"
        from_number = "+15855846197"
        client.messages.create(
            to=to_number,
            from_=from_number,
            body=message)
        success_label.config(text="SMS sent successfully!")
    else:
        success_label.config(text="Please enter some text.")
# Create a Folium map
m = folium.Map(location=[18.5204, 73.8567], zoom_start=12)  # Set default starting point to Pune

def calculate_distance(lat1, lon1, lat2, lon2):
    # The radius of the Earth in kilometers
    radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    cord = getLoc()
    lat1 = cord[0]
    lon1 = cord[1]
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians()
    lon2_rad = radians(lon2)

    # Calculate the differences between the latitude and longitude coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula to calculate the distance
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    return distance

# Function to display the map with the markers
def display_route():
    destination = add.get()
    # Geocode the starting point and destination
    geolocator = Nominatim(user_agent='my_app')
    start_location = geolocator.geocode("Pune")
    dest_location = geolocator.geocode(destination)

    if dest_location is None:
        return

    # Add markers for the starting point and destination
    start_marker = folium.Marker(location=[start_location.latitude, start_location.longitude], tooltip='Start',
                                icon=folium.Icon(color='blue'))
    dest_marker = folium.Marker(location=[dest_location.latitude, dest_location.longitude], tooltip='Destination',
                               icon=folium.Icon(color='red'))

    m.add_child(start_marker)
    m.add_child(dest_marker)

    # Fit the map to the markers
    m.fit_bounds(m.get_bounds())

    # Save the map as HTML
    m.save('map.html')

    # Open the HTML map in the default web browser
    webbrowser.open('map.html')
    print(dest_location)
    print(dest_location.latitude)
    print(dest_location.longitude)


def replace_button():
    button.destroy()  # Remove Button 1
    button1.pack(pady=20) # Display Button 2
    button1.bind("<Enter>", lambda event: button1.config(width=12, height=1, bg='#D3D3D3'))
    button1.bind("<Leave>", lambda event: button1.config(width=10, height=1, bg='SystemButtonFace'))


# Create button to execute code
button_font = ("TkDefaultFont", 15)  # specify the font size here
button = tk.Button(text="Find A Ride", command=replace_button, width=10, height=1,  font=button_font)
button.pack(pady=20)
button.bind("<Enter>", lambda event: button.config(width=12, height=1,bg='#D3D3D3'))
button.bind("<Leave>", lambda event: button.config(width=10, height=1,bg='SystemButtonFace'))
button1_font = ("TkDefaultFont", 15)  # specify the font size here
button1 = tk.Button(text="Book A Ride", command=display_route, width=10, height=1,  font=button_font)

# Create label for success message
success_label = tk.Label(text="")
success_label.pack()