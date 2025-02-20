import random
import string
import tkinter as tk
from tkinter import messagebox
import csv

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to save passwords to a CSV file
def save_to_csv(passwords, filename="passwords.csv"):
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Passwords"])
            for pwd in passwords:
                writer.writerow([pwd])
        messagebox.showinfo("Success", f"Passwords saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

# Function to load passwords from a CSV file
def load_from_csv(filename="passwords.csv"):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return [row[0] for row in reader]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return []

# Function to generate passwords and display them in the GUI
def generate_and_display():
    try:
        num = int(entry_count.get())
        length = int(entry_length.get())
        passwords = [generate_password(length) for _ in range(num)]
        listbox.delete(0, tk.END)
        for pwd in passwords:
            listbox.insert(tk.END, pwd)
        save_to_csv(passwords)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for count and length.")

# Basic GUI setup using tkinter
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x400")

tk.Label(root, text="Number of Passwords:").pack()
entry_count = tk.Entry(root)
entry_count.pack()

tk.Label(root, text="Password Length:").pack()
entry_length = tk.Entry(root)
entry_length.pack()

tk.Button(root, text="Generate", command=generate_and_display).pack()

tk.Button(root, text="Load Saved Passwords", command=lambda: listbox.insert(tk.END, *load_from_csv())).pack()

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack()

root.mainloop()
