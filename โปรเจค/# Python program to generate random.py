import random
import pyperclip
import csv
from tkinter import *
from tkinter.ttk import *

# Function to generate password
def generate_password():
    entry.delete(0, END)
    length = var1.get()

    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password = ""

    if var.get() == 1:
        password = ''.join(random.choice(lower) for _ in range(length))
    elif var.get() == 0:
        password = ''.join(random.choice(upper) for _ in range(length))
    elif var.get() == 3:
        password = ''.join(random.choice(digits) for _ in range(length))
    else:
        print("Please choose an option")

    entry.insert(0, password)
    return password

# Function to copy password
def copy_to_clipboard():
    pyperclip.copy(entry.get())

# Function to save password to CSV
def save_to_csv():
    password = entry.get()
    if password:
        with open("passwords.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Generated Password", password])
        print("Password saved to CSV!")

# Main GUI
root = Tk()
root.title("Password Generator")
root.geometry("400x250")  # Set window size
root.resizable(False, False)  # Fix window size

# Apply ttk theme
style = Style()
style.configure("TButton", padding=5, font=("Arial", 10))
style.configure("TLabel", font=("Arial", 10))
style.configure("TEntry", padding=5, font=("Arial", 10))

# Variables
var = IntVar()
var1 = IntVar(value=8)  # Default length

# Title Label
Label(root, text="Random Password Generator", font=("Arial", 14, "bold")).pack(pady=10)

# Password Entry + Buttons
frame1 = Frame(root)
frame1.pack(pady=5)

Label(frame1, text="Password:").pack(side=LEFT, padx=5)
entry = Entry(frame1, width=25)
entry.pack(side=LEFT, padx=5)

Button(frame1, text="Copy", command=copy_to_clipboard).pack(side=LEFT, padx=2)
Button(frame1, text="Save", command=save_to_csv).pack(side=LEFT, padx=2)

# Length Selection
frame2 = Frame(root)
frame2.pack(pady=5)

Label(frame2, text="Length:").pack(side=LEFT, padx=5)
combo = Combobox(frame2, textvariable=var1, width=5)
combo['values'] = tuple(range(8, 36))
combo.current(0)
combo.pack(side=LEFT, padx=5)

# Strength Selection
frame3 = Frame(root)
frame3.pack(pady=5)

Label(frame3, text="Strength:").pack(side=LEFT, padx=5)
Radiobutton(frame3, text="Low", variable=var, value=1).pack(side=LEFT, padx=5)
Radiobutton(frame3, text="Medium", variable=var, value=0).pack(side=LEFT, padx=5)
Radiobutton(frame3, text="Strong", variable=var, value=3).pack(side=LEFT, padx=5)

# Generate Button
Button(root, text="Generate Password", command=generate_password).pack(pady=10)

# Start GUI
root.mainloop()
