import customtkinter
import tkinter
import datetime
import csv
import pandas as pd
from PIL import ImageTk, Image
import admin
import staff_work
from operations import Operations

def login():
  ops=Operations()
  un=username.get()
  pw=password.get()
  is_admin=is_super_admin.get()
  data=ops.login(un,pw,is_admin)
  if data and not is_admin:
    print(data)
    login_page.destroy()
    staff_work.staff_work(un)
  elif data and is_admin:
    print(data)
    login_page.destroy()
    admin.admin()
  else:
    login_label.configure(text="wrong credentials")
  


# Set appearance mode and default color theme

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Initialize login window
login_page = customtkinter.CTk()
login_page.title("OutSourcery")
login_page.geometry("350x250")  # Adjusted height for extra space
login_page.resizable(False, False)  # Disable window resizing

font = ("Times New Roman", 15, "bold")

# Frames
main_frame = customtkinter.CTkFrame(login_page)
main_frame.place(x=0, y=0, relheight=1, relwidth=1)

# Labels and Entry Fields
customtkinter.CTkLabel(main_frame, text="Username", font=font).grid(row=0, column=0, padx=(20, 0), pady=(20, 10))
customtkinter.CTkLabel(main_frame, text="Password", font=font).grid(row=1, column=0, padx=(20, 0), pady=(10, 10))

username = customtkinter.CTkEntry(main_frame, placeholder_text="Username", width=210)
username.grid(row=0, column=1, padx=(20, 0), pady=(20, 10))

password = customtkinter.CTkEntry(main_frame, placeholder_text="Password", show="*", width=210)
password.grid(row=1, column=1, padx=(20, 0), pady=(10, 10))

# Checkbox for "Is Super Admin"
is_super_admin = customtkinter.BooleanVar()  # Boolean variable to track checkbox state
super_admin_checkbox = customtkinter.CTkCheckBox(
    main_frame, text="Is Super Admin?", variable=is_super_admin, font=("Arial", 13)
)
super_admin_checkbox.grid(row=2, column=1, padx=(20, 0), pady=(10, 10))
customtkinter.CTkButton(main_frame, text="Login", command=login).grid(row=3, column=1, padx=(20, 0), pady=(20, 10))

# Login status label
login_label = customtkinter.CTkLabel(main_frame, text="", font=font)
login_label.grid(row=4, column=1, padx=(20, 0), pady=(10, 20))

login_page.mainloop()
