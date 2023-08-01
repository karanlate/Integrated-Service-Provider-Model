import tkinter as tk
from twilio.rest import Client
import asyncio
import winsdk.windows.devices.geolocation as wdg

def show(root):
    # Create the option page widgets
    label = tk.Label(root)
    label.pack(pady=20)

# Create input label
label_font = ("TkDefaultFont", 15)
input_label = tk.Label(text="Enter Contact Number, Address And Which Type Of Help Do You Want?",font=label_font)
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
add.insert(0, "Enter Address Here...")
def on_add_click(event):
    if add.get() == "Enter Address Here...":
        add.delete(0, "end")  # delete all the text in the entry
        add.insert(0, "")  # insert blank for user input
# bind the on_entry_click function to the entry widget
add.bind("<FocusIn>", on_add_click)
add.pack()
# Create a Text widget
text_widget = tk.Text(height=16, width=100, font=("TkDefaultFont", 12))
text_widget.insert('1.0', 'Enter Which Type Of Help Do You Want???')
# remove placeholder text when user starts typing
def on_text_click(event):
    if text_widget.get('1.0', 'end-1c') == 'Enter Which Type Of Help Do You Want???':
        text_widget.delete('1.0', 'end-1c')  # delete the placeholder text
# bind the on_text_click function to the Text widget
text_widget.bind('<FocusIn>', on_text_click)
# Add the Text widget to the window
text_widget.pack()


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
    text3 = text_widget.get("1.0", "end-1c")
    if text1 and text2 and text3:
        cord = getLoc()
        lat = cord[0]
        lon = cord[1]
        message = "My current location is: https://www.google.com/maps/search/?api=1&query=" + str(lat) + "," + str(
            lon) + "\n" + "Customer Contact Number :" + str(text1) + "\n" + "Address :" + str(text2) + "\n" + "Job Description :" + str(text3)
        to_number = "+917397805884"
        from_number = "+15855846197"
        client.messages.create(
            to=to_number,
            from_=from_number,
            body=message)
        success_label.config(text="SMS sent successfully!")
    else:
        success_label.config(text="Please enter some text.")


# Create button to execute code
button_font = ("TkDefaultFont", 30)  # specify the font size here
button = tk.Button(text="Send Location SMS", command=sendLocationSMS, width=22, height=1,  font=button_font)
button.pack(pady=20)
button.bind("<Enter>", lambda event: button.config(width=23, height=2,bg='#D3D3D3'))
button.bind("<Leave>", lambda event: button.config(width=22, height=1,bg='SystemButtonFace'))

# Create label for success message
success_label = tk.Label(text="")
success_label.pack()

