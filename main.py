import json
from os.path import exists
from tkinter import *
from tkinter import messagebox
from random_password import RandomPassword
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password_generator():
    new_password = RandomPassword()
    pyperclip.copy(new_password.password)
    print(new_password.password)
    password_entry.delete(0, END)
    password_entry.insert(0, new_password.password)


# ---------------------------- SAVE PASSWORD AND SEARCH DATA ------------------------------- #
def save():
    if (not website_entry.get() or website_entry.get().isspace() or not email_entry.get() or email_entry.get().isspace()
            or not password_entry.get() or password_entry.get().isspace()):
        messagebox.showinfo(title="Empty fields", message="Hey you left some fields empty,\n"
                                                          "make sure to fill all the fields before saving")

    else:
        is_ok = messagebox.askokcancel(title=website_entry.get(), message=f"website entered: {website_entry.get()}\n"
                                                                          f"email entered: {email_entry.get()}\n"
                                                                          f"password entered: {password_entry.get()}\n"
                                                                          f"is it ok?")

        if is_ok:
            website = website_entry.get().lower()
            email = email_entry.get()
            password = password_entry.get()
            new_data = {
                website: {
                    "email": email,
                    "password": password,
                }}
            try:
                with open("logins_data.json", mode="r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("logins_data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            except json.decoder.JSONDecodeError:
                with open("logins_data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)
                with open("logins_data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)


# search entries
def search_data():
    search_website = website_entry.get().lower()
    with open("logins_data.json", mode="r") as data_file:
        data = json.load(data_file)
    try:  # tries to see if entries exist in the json data fie
        found_email = data.get(search_website).get("email")
        found_password = data.get(search_website).get("password")
        print(data.get(search_website).get("email") + " " + data.get(search_website).get("password"))
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        messagebox.showinfo(title="Found entry", message=f"Email: {found_email}\n"
                                                         f"Password: {found_password}")
    except AttributeError:  # did not find any entries notify the user
        messagebox.showinfo(title="Failed to find entry", message=f"Did not find any '{search_website}' entries"
                                                                  " please check for spelling")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass")
screen_width = window.winfo_screenwidth()  # Width of the screen
screen_height = window.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - 280
y = (screen_height / 2) - 400

window.geometry('%dx%d+%d+%d' % (560, 420, x, y))
# photo
canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
window.config(padx=20, pady=20, bg="white")
canvas.grid(row=0, column=1)
image_logo = PhotoImage(file="lol.ppm")
canvas.create_image(100, 100, image=image_logo)

# titles
website_title = Label(text="Website:", font=("ariel", 14), anchor="center", width=16, bg="white", fg="black")
website_title.grid(row=1, column=0)
website_title = Label(text="Email/Username:", font=("ariel", 14), anchor="center", width=16, bg="white", fg="black")
website_title.grid(row=2, column=0)
website_title = Label(text="Password:", font=("ariel", 14), anchor="center", width=16, bg="white", fg="black")
website_title.grid(row=3, column=0)

# entries
website_entry = Entry(width=21, fg="black", bg="#F5EDDC", highlightthickness=0)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35, fg="black", bg="#F5EDDC", highlightthickness=0)
email_entry.grid(row=2, column=1, columnspan=3)
password_entry = Entry(width=21, fg="black", bg="#F5EDDC", highlightthickness=0)
password_entry.grid(row=3, column=1)

# buttons
generate_button = Button(text="Generate", bg="white", width=9, highlightbackground="white",
                         command=random_password_generator)
generate_button.grid(row=3, column=3, columnspan=2, pady=8)
add_button = Button(text="Add", bg="white", width=33, highlightbackground="white", command=save)
add_button.grid(row=4, column=1, columnspan=3, pady=8)
search_button = Button(text="Search", bg="white", width=9, highlightbackground="white",
                       command=search_data)
search_button.grid(row=1, column=3, pady=8)

file_exists = exists("login_email.txt")


# set email as default entry text
def get_email():
    with open("login_email.txt", mode="r", encoding="ascii") as file:
        email_entry.delete(0, END)
        email_entry.insert(0, file.read())


# save the email to a text file
def write_new_email(email):
    with open("login_email.txt", mode="w", encoding="ascii") as file:
        file.write(email)

    get_email()


# new email window
def new_email():
    # top.destroy()
    second_top = Toplevel(window)
    second_top.attributes("-topmost", True)
    screen_width = second_top.winfo_screenwidth()  # Width of the screen
    screen_height = second_top.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - 280
    y = (screen_height / 2) - 360
    second_top.geometry('%dx%d+%d+%d' % (570, 90, x, y))
    second_top.title("new email")
    new_email_label = Label(second_top, text="Please enter an email:")
    new_email_label.grid(row=0, column=1, pady=10)
    new_email_entry = Entry(second_top, width=20)
    new_email_entry.grid(row=0, column=2, columnspan=2, pady=10)
    confirm_email_button = Button(second_top, text="confirm email",
                                  command=lambda: [write_new_email(new_email_entry.get()), second_top.destroy()])
    confirm_email_button.grid(row=1, column=4, pady=0, padx=10)
    cancel_email = Button(second_top, text="cancel", command=second_top.destroy)
    cancel_email.grid(row=1, column=0, pady=5, padx=10)


# if the user never created a save file we will ask the user if he wants to save a default email address
if not file_exists:
    top = Toplevel(window)
    top.attributes("-topmost", True)
    screen_width = top.winfo_screenwidth()  # Width of the screen
    screen_height = top.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - 130
    y = (screen_height / 2) - 360

    top.geometry('%dx%d+%d+%d' % (300, 150, x, y))
    top.title("Welcome!")
    welcome_label = Label(top, text="Hold on! no email found\n "
                                    "click the new email button to use a static email\n"
                                    " or click 'no thanks' to use"
                                    " a dynamic email")
    welcome_label.grid(row=0, column=0, columnspan=2, rowspan=2, pady=20)
    new_email_button = Button(top, text="new email", command=lambda: [new_email(), top.destroy()])
    new_email_button.grid(row=2, column=1, pady=5, padx=20)
    cancel_button = Button(top, text="no thanks", command=top.destroy)
    cancel_button.grid(row=2, column=0, pady=0, padx=20)
if file_exists:
    get_email()
add_button = Button(text="Save new email", bg="white", width=33, highlightbackground="white", command=new_email)
add_button.grid(row=5, column=1, columnspan=3)
window.wm_iconphoto(False, image_logo)

window.mainloop()
