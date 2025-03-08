import tkinter as tk
from tkinter import ttk, messagebox
import csv

CSV_FILE = "bookings.csv"

def save_to_csv(data):
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "ห้องประชุม", "วันที่", "เวลา", "ผู้จอง"])
        for i, row in enumerate(data, start=1):
            row[0] = i  # Update ID
            writer.writerow(row)

def load_bookings():
    tree.delete(*tree.get_children())
    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

def add_booking():
    room = room_var.get()
    date = f"{day_var.get()}/{month_var.get()}/{year_var.get()}"
    time = time_var.get()
    booked_by = entry_name.get()
    
    if not (room and date and time and booked_by):
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน!")
        return
    
    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row[1] == room and row[2] == date and row[3] == time:
                    messagebox.showwarning("แจ้งเตือน", "ห้องนี้ถูกจองแล้ว!")
                    return
    except FileNotFoundError:
        pass
    
    booking_data = load_csv_data()
    booking_data.append([len(booking_data) + 1, room, date, time, booked_by])
    save_to_csv(booking_data)
    messagebox.showinfo("สำเร็จ", "เพิ่มการจองสำเร็จ!")
    clear_entries()
    load_bookings()

def delete_booking():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกการจองที่ต้องการลบ")
        return
    booking_id = tree.item(selected_item)['values'][0]
    booking_data = [row for row in load_csv_data() if row[0] != str(booking_id)]
    save_to_csv(booking_data)
    messagebox.showinfo("สำเร็จ", "ลบการจองสำเร็จ!")
    load_bookings()

def load_csv_data():
    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader, None)
            return list(reader)
    except FileNotFoundError:
        return []

def clear_entries():
    entry_name.delete(0, tk.END)
    room_var.set(rooms[0])
    time_var.set(times[0])
    day_var.set("1")
    month_var.set("1")
    year_var.set("2025")

root = tk.Tk()
root.title("ระบบจองห้องประชุม")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="raised", bd=2)
frame.pack(pady=20)

rooms = ["ห้อง A", "ห้อง B", "ห้อง C", "ห้อง D"]
times = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "13:00-14:00", "14:00-15:00"]

room_var = tk.StringVar(value=rooms[0])
time_var = tk.StringVar(value=times[0])
day_var = tk.StringVar(value="1")
month_var = tk.StringVar(value="1")
year_var = tk.StringVar(value="2025")

tk.Label(frame, text="ห้องประชุม:", bg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
tk.OptionMenu(frame, room_var, *rooms).grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="วันที่:", bg="#ffffff").grid(row=1, column=0, padx=10, pady=5)
date_frame = tk.Frame(frame, bg="#ffffff")
date_frame.grid(row=1, column=1, columnspan=3, pady=5)
tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)]).pack(side=tk.LEFT, padx=2)
tk.OptionMenu(date_frame, month_var, *[str(i) for i in range(1, 13)]).pack(side=tk.LEFT, padx=2)
tk.OptionMenu(date_frame, year_var, *[str(i) for i in range(2025, 2035)]).pack(side=tk.LEFT, padx=2)

tk.Label(frame, text="เวลา:", bg="#ffffff").grid(row=2, column=0, padx=10, pady=5)
tk.OptionMenu(frame, time_var, *times).grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="ชื่อผู้จอง:", bg="#ffffff").grid(row=3, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=3, column=1, padx=10, pady=5)

tk.Button(frame, text="เพิ่มการจอง", command=add_booking, bg="#4CAF50", fg="white").grid(row=4, column=0, pady=10)
tk.Button(frame, text="ลบการจอง", command=delete_booking, bg="#f44336", fg="white").grid(row=4, column=2, pady=10)

columns = ("ID", "ห้องประชุม", "วันที่", "เวลา", "ผู้จอง")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(expand=True, fill="both", padx=20, pady=20)

load_bookings()
root.mainloop()
