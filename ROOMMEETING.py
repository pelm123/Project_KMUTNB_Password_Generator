import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os

CSV_FILE = "bookings.csv"

def save_to_csv(data):
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "ห้องประชุม", "วันที่", "เวลา", "ผู้จอง"])
        for i, row in enumerate(data, start=1):
            row[0] = i  # อัปเดต ID
            writer.writerow(row)

def load_bookings():
    tree.delete(*tree.get_children())
    if not os.path.exists(CSV_FILE):
        return
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        rows = list(reader)
    for row in rows:
        tree.insert("", "end", values=row)

def is_duplicate_booking(room, date, time):
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[1] == room and row[2] == date and row[3] == time:
                return True
    return False

def add_booking():
    room, date, time, booked_by = room_var.get(), date_entry.get(), time_var.get(), entry_name.get()
    if not (room and date and time and booked_by):
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน!")
        return
    if is_duplicate_booking(room, date, time):
        messagebox.showwarning("แจ้งเตือน", "ห้องนี้ถูกจองในช่วงเวลานี้แล้ว!")
        return
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
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        return list(reader)

def clear_entries():
    entry_name.delete(0, tk.END)
    room_var.set(rooms[0])
    time_var.set(times[0])

root = tk.Tk()
root.title("ระบบจองห้องประชุม")
root.geometry("700x600")
root.config(bg="#f0f0f0")

frame_top = tk.Frame(root, bg="#d9edf7", padx=10, pady=10)
frame_top.pack(fill="x")

tk.Label(frame_top, text="เลือกห้องประชุม:", bg="#d9edf7").grid(row=0, column=0, padx=5, pady=5)
rooms = ["ห้อง A", "ห้อง B", "ห้อง C", "ห้อง D"]
room_var = tk.StringVar(value=rooms[0])
ttk.Combobox(frame_top, textvariable=room_var, values=rooms).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_top, text="เลือกวันที่:", bg="#d9edf7").grid(row=1, column=0, padx=5, pady=5)
date_entry = DateEntry(frame_top, width=12, background="darkblue", foreground="white", borderwidth=2)
date_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_top, text="เลือกช่วงเวลา:", bg="#d9edf7").grid(row=2, column=0, padx=5, pady=5)
times = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "13:00-14:00", "14:00-15:00"]
time_var = tk.StringVar(value=times[0])
ttk.Combobox(frame_top, textvariable=time_var, values=times).grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_top, text="ชื่อผู้จอง:", bg="#d9edf7").grid(row=3, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_top)
entry_name.grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame_top, text="เพิ่มการจอง", command=add_booking, bg="#5cb85c", fg="white").grid(row=4, column=0, padx=5, pady=10)
tk.Button(frame_top, text="ลบการจอง", command=delete_booking, bg="#d9534f", fg="white").grid(row=4, column=1, padx=5, pady=10)

columns = ("ID", "ห้องประชุม", "วันที่", "เวลา", "ผู้จอง")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(expand=True, fill="both", padx=10, pady=10)

load_bookings()
root.mainloop()
