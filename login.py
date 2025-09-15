# login.py
import tkinter as tk
from tkinter import messagebox
import subprocess  # used to open another python file

def login():
    user = entry_user.get()
    pwd = entry_pass.get()
    # Simple login check
    if user == "admin" and pwd == "123":
        messagebox.showinfo("Login Success", "Welcome to Dashboard!")
        root.destroy()
        subprocess.Popen(["python", "dashboard.py"])  # open dashboard.py
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# Tkinter GUI for Login
root = tk.Tk()
root.title("Login System")
root.geometry("300x200")

tk.Label(root, text="Username").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack(pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()