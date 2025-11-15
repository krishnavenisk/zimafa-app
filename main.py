import tkinter as tk
from tkinter import messagebox
from database import init_db, validate_user
from client_module import open_client_window   # VERY IMPORTANT


# Initialize database
init_db()


# Login Function
def login():
    username = entry_username.get()
    password = entry_password.get()

    user = validate_user(username, password)
    if user:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        root.destroy()
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")


# Dashboard Window
def open_dashboard(username):
    dash = tk.Tk()
    dash.title("Zimafa Interior Designs - Dashboard")
    dash.geometry("400x350")

    label = tk.Label(dash, text=f"Welcome {username}", font=("Arial", 16))
    label.pack(pady=20)

    # ---------- CLIENT MODULE BUTTON ----------
    btn_client = tk.Button(
        dash,
        text="Client Management",
        width=20,
        bg="#0077E6",
        fg="white",
        command=open_client_window
    )
    btn_client.pack(pady=15)

    dash.mainloop()


# ------------------------
# LOGIN WINDOW
# ------------------------
root = tk.Tk()
root.title("Zimafa Interior Designs - Login")
root.geometry("350x250")

label_title = tk.Label(root, text="User Login", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

label_user = tk.Label(root, text="Username:")
label_user.pack()
entry_username = tk.Entry(root, width=25)
entry_username.pack(pady=5)

label_pass = tk.Label(root, text="Password:")
label_pass.pack()
entry_password = tk.Entry(root, show="*", width=25)
entry_password.pack(pady=5)

btn_login = tk.Button(root, text="Login", width=15,
                      command=login, bg="#4CAF50", fg="white")
btn_login.pack(pady=15)

root.mainloop()
