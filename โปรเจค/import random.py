import random
import string
import tkinter as tk
from tkinter import messagebox
import csv
import base64

# Function to generate a random password
def generate_password(length=12, use_digits=True, use_lower=True, use_upper=True, use_special=True):
    length = max(length, 12)
    characters = "".join([
        string.digits if use_digits else "",
        string.ascii_lowercase if use_lower else "",
        string.ascii_uppercase if use_upper else "",
        string.punctuation if use_special else ""
    ])
    return "".join(random.choice(characters) for _ in range(length)) if characters else "No character set selected"

# Function to save passwords to a CSV file with Base64 encoding
# Function to save passwords to a CSV file WITHOUT Base64 encoding
def save_to_csv(passwords, filename="passwords.csv"):
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Name", "Passwords"])  
            for name, pwd in passwords:
                print(f"Saving: {name} -> {pwd}")  # Debug print
                writer.writerow([name, pwd])  # บันทึกโดยตรง
        messagebox.showinfo("Success", "Passwords saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")


# Function to load passwords from a CSV file
# Function to load passwords from a CSV file WITHOUT decoding Base64
def load_from_csv(filename="passwords.csv"):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # ข้าม Header
            loaded_passwords = []
            for row in reader:
                print(f"Loading: {row[0]} -> {row[1]}")  # Debug print
                loaded_passwords.append(f"{row[0]}: {row[1]}")  # ไม่ต้องถอดรหัส
            return loaded_passwords
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return []



# Function to generate and display passwords
def generate_and_display():
    try:
        num, length = int(entry_count.get()), int(entry_length.get())
        passwords = [(entry_name.get() or f"Password_{i+1}", generate_password(length, var_digits.get(), var_lower.get(), var_upper.get(), var_special.get())) for i in range(num)]
        listbox.delete(0, tk.END)
        for name, pwd in passwords:
            listbox.insert(tk.END, f"{name}: {pwd}")
        save_to_csv(passwords)
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numbers for count and length.")

# Function to copy selected password
def copy_password():
    try:
        selected = listbox.get(listbox.curselection())
        root.clipboard_clear()
        root.clipboard_append(selected.split(": ", 1)[1])
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    except:
        messagebox.showwarning("No Selection", "Select a password to copy.")

# Function to delete selected password from listbox
def delete_selected():
    try:
        listbox.delete(listbox.curselection())
    except:
        messagebox.showwarning("No Selection", "Select a password to delete.")

# GUI Setup
root = tk.Tk()
root.title("Password Generator")
root.geometry("420x600")
root.configure(bg="#2C3E50")

tk.Label(root, text="Password Name:", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
entry_name = tk.Entry(root)
entry_name.pack(pady=2)

tk.Label(root, text="Number of Passwords:", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
entry_count = tk.Entry(root)
entry_count.pack(pady=2)

tk.Label(root, text="Password Length (Min 12):", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
entry_length = tk.Entry(root)
entry_length.pack(pady=2)

var_digits, var_lower, var_upper, var_special = (tk.BooleanVar(value=True) for _ in range(4))
for text, var in [("Include Digits", var_digits), ("Include Lowercase Letters", var_lower), ("Include Uppercase Letters", var_upper), ("Include Special Characters", var_special)]:
    tk.Checkbutton(root, text=text, variable=var, bg="#2C3E50", fg="white").pack()

for text, cmd in [("Generate", generate_and_display), ("Load Saved Passwords", lambda: listbox.insert(tk.END, *load_from_csv())), ("Copy Selected Password", copy_password), ("Delete Selected", delete_selected)]:
    tk.Button(root, text=text, command=cmd, bg="#16A085", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=5)

listbox = tk.Listbox(root, width=50, height=10, bg="#ECF0F1", fg="black", font=("Arial", 10))
listbox.pack(pady=5)

root.mainloop()