import random
import string
import tkinter as tk
import csv

# Function to generate a random password
def generate_password(length=12, use_digits=True, use_lower=True, use_upper=True, use_special=True):
    if length < 12:
        length = 12  # Ensure minimum length of 12
    
    characters = ""
    if use_digits:
        characters += string.digits
    if use_lower:
        characters += string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_special:
        characters += string.punctuation
    
    if not characters:
        return "No character set selected"
    
    return ''.join(random.choice(characters) for _ in range(length))

# Function to save passwords to a CSV file without overwriting existing entries
def save_to_csv(passwords, filename="passwords.csv"):
    try:
        file_exists = False
        try:
            with open(filename, mode='r') as file:
                file_exists = True
        except FileNotFoundError:
            pass
        
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Passwords"])
            for name, pwd in passwords:
                writer.writerow([name, pwd])
        print(f"Passwords saved to {filename}")
    except Exception as e:
        print(f"Failed to save file: {e}")

# Function to load passwords from a CSV file
def load_from_csv(filename="passwords.csv"):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return [f"{row[0]}: {row[1]}" for row in reader]
    except Exception as e:
        print(f"Failed to read file: {e}")
        return []

# Function to generate passwords and display them in the GUI
def generate_and_display():
    try:
        num = int(entry_count.get())
        length = int(entry_length.get())
        if length < 12:
            length = 12  # Ensure minimum length of 12
        
        passwords = [(entry_name.get() or f"Password_{i+1}", generate_password(length, var_digits.get(), var_lower.get(), var_upper.get(), var_special.get())) for i in range(num)]
        listbox.delete(0, tk.END)
        for name, pwd in passwords:
            listbox.insert(tk.END, f"{name}: {pwd}")
        save_to_csv(passwords)
    except ValueError:
        print("Input Error: Please enter valid numbers for count and length.")

# Basic GUI setup using tkinter
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x500")

tk.Label(root, text="Password Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Number of Passwords:").pack()
entry_count = tk.Entry(root)
entry_count.pack()

tk.Label(root, text="Password Length (Minimum 12):").pack()
entry_length = tk.Entry(root)
entry_length.pack()

var_digits = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Digits", variable=var_digits).pack()
tk.Checkbutton(root, text="Include Lowercase Letters", variable=var_lower).pack()
tk.Checkbutton(root, text="Include Uppercase Letters", variable=var_upper).pack()
tk.Checkbutton(root, text="Include Special Characters", variable=var_special).pack()

tk.Button(root, text="Generate", command=generate_and_display).pack()

tk.Button(root, text="Load Saved Passwords", command=lambda: listbox.insert(tk.END, *load_from_csv())).pack()

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack()

root.mainloop()
