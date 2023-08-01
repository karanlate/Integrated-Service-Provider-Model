import tkinter as tk
import sqlite3
import importlib.util

class LoginSignupWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Integrated Service Provider Model")
        self.geometry("1200x600")  # width x height
        self.create_login_signup_widgets()
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        # create a label for the message
        self.message_label = tk.Label(self, text="")
        self.message_label.pack(pady=10)

    def create_login_signup_widgets(self):
        # Remove all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()
        self.label_font = ("TkDefaultFont", 30)
        self.input_label = tk.Label(self, text="Integrated Service Provider Model Login / SignUp Panel", font=self.label_font)
        self.input_label.pack(pady=10)

        self.username_label = tk.Label(self, text="Username:", font=("TkDefaultFont", 25))
        self.username_label.pack()
        self.username_entry = tk.Entry(self, width=40, font=("TkDefaultFont", 18))
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:", font=("TkDefaultFont", 25))
        self.password_label.pack()
        self.password_entry = tk.Entry(self, width=40, font=("TkDefaultFont", 18), show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login, font=("TkDefaultFont", 15), width=10)
        self.login_button.pack(pady=10)
        self.login_button.bind("<Enter>", lambda event: self.login_button.config(width=12, height=2, bg='#D3D3D3'))
        self.login_button.bind("<Leave>", lambda event: self.login_button.config(width=10, height=1, bg='SystemButtonFace'))

        self.signup_button = tk.Button(self, text="Sign up", command=self.open_signup_window, font=("TkDefaultFont", 15), width=10)
        self.signup_button.pack(pady=10)
        self.signup_button.bind("<Enter>", lambda event: self.signup_button.config(width=12, height=2, bg='#D3D3D3'))
        self.signup_button.bind("<Leave>", lambda event: self.signup_button.config(width=10, height=1, bg='SystemButtonFace'))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            message = "Please Enter Username And Password"  # Replace with your desired message
            self.message_label.config(text=message)

            return

        # Check if the username and password match a user in the database
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            self.show_main_menu()
        else:
            message = "Invalid username or password"  # Replace with your desired message
            self.message_label.config(text=message)

    def open_signup_window(self):
        SignupWindow(self)

    def show_main_menu(self):
        # Remove all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()

        title_font = ("TkDefaultFont", 30, "bold")
        title_label = tk.Label(self, text="Integrated Service Provider Model", font=title_font)
        title_label.pack(side="top", pady=20)

        button_font = ("TkDefaultFont", 30)
        option1 = tk.Button(self, text="Order Food", command=lambda: self.show_option_page("order food"), width=15, height=2, font=button_font)
        option1.pack(pady=10)
        option1.bind("<Enter>", lambda event: option1.config(width=16, height=3, bg="#D3D3D3"))
        option1.bind("<Leave>", lambda event: option1.config(width=15, height=2, bg="SystemButtonFace"))

        option2 = tk.Button(self, text="Book A Ride", command=lambda: self.show_option_page("book a ride"), width=15, height=2, font=button_font)
        option2.pack(pady=10)
        option2.bind("<Enter>", lambda event: option2.config(width=16, height=3, bg="#D3D3D3"))
        option2.bind("<Leave>", lambda event: option2.config(width=15, height=2, bg="SystemButtonFace"))

        option3 = tk.Button(self, text="Call For Help", command=lambda: self.show_option_page("call for help"), width=15, height=2, font=button_font)
        option3.pack(pady=10)
        option3.bind("<Enter>", lambda event: option3.config(width=16, height=3, bg="#D3D3D3"))
        option3.bind("<Leave>", lambda event: option3.config(width=15, height=2, bg="SystemButtonFace"))

    def show_option_page(self, option_name):
        # Remove all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()

        # Create the "Home" button
        home_button = tk.Button(self, text="Home", command=self.show_main_menu, width=8, height=2)
        home_button.pack(side="top", padx=10, pady=10)
        home_button.bind("<Enter>", lambda event: home_button.config(width=10, height=3, bg="#D3D3D3"))
        home_button.bind("<Leave>", lambda event: home_button.config(width=8, height=2, bg="SystemButtonFace"))
        logout_frame = tk.Frame(self)
        # create the logout button inside the frame
        logout_frame.place(anchor="ne", relx=1.0, x=-20, y=0)
        logout_button = tk.Button(logout_frame, text="Logout", command=self.create_login_signup_widgets, width=7,height=1)
        logout_button.pack()
        logout_button.bind("<Enter>", lambda event: logout_button.config(width=9, height=2, bg="#D3D3D3"))
        logout_button.bind("<Leave>", lambda event: logout_button.config(width=7, height=1, bg="SystemButtonFace"))
        # Get the path for the option page
        option_path = f"options/{option_name}.py"

        # Load the option module
        spec = importlib.util.spec_from_file_location(option_name, option_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call the option module's show() function
        module.show(self)

class SignupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sign Up")
        self.geometry("400x300")
        self.parent = parent
        self.create_signup_widgets()
        # create a label for the message
        self.message_label = tk.Label(self, text="")
        self.message_label.pack(pady=10)

    def create_signup_widgets(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # create a label and entry box for the email
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        # create a label and entry box for the age
        self.age_label = tk.Label(self, text="Age:")
        self.age_label.pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack()

        self.signup_button = tk.Button(self, text="Sign up", command=self.signup)
        self.signup_button.pack(pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Insert the new user into the database
        self.parent.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.parent.conn.commit()

        if not username or not password:
            message = "Invalid input. Please fill in all fields."  # Replace with your desired message
            self.message_label.config(text=message)
            return

            # Save the signup data to the database or perform any other required actions
            # ...

        message = "Signup successful."  # Replace with your desired message
        self.message_label.config(text=message)
        self.destroy()

if __name__ == "__main__":
    app = LoginSignupWindow()
    app.mainloop()