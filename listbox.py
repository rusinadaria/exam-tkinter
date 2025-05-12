import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://localhost:8080/api/partners"
ADD_URL = "http://localhost:8080/api/addPartner"

def fetch_partners():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        partners = response.json()
        for widget in list_frame.winfo_children():
            widget.destroy()
        for partner in partners:
            frame = ttk.LabelFrame(list_frame, text="Партнёр", padding=10)
            label = ttk.Label(frame, text=partner)
            label.pack()
            frame.pack(fill='x', padx=10, pady=5)
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные:\n{e}")

def open_add_partner_window():
    add_window = tk.Toplevel(root)
    add_window.title("Добавить партнёра")
    add_window.geometry("300x200")

    tk.Label(add_window, text="Имя:").pack(pady=5)
    name_entry = ttk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Телефон:").pack(pady=5)
    phone_entry = ttk.Entry(add_window)
    phone_entry.pack()

    def submit():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return
        try:
            response = requests.post(ADD_URL, json={"name": name, "phone": phone})
            response.raise_for_status()
            messagebox.showinfo("Успех", "Партнёр добавлен")
            add_window.destroy()
            fetch_partners()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить партнёра:\n{e}")

    # ttk.Button(add_window, text="Сохранить", command=submit).pack(pady=10)
    # Кнопки
    btn_frame = ttk.Frame(add_window)
    btn_frame.pack(pady=15)

    ttk.Button(btn_frame, text="Сохранить", command=submit).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Назад", command=add_window.destroy).grid(row=0, column=1, padx=5)

# Создание окна
root = tk.Tk()
root.title("Список партнёров")
root.geometry("400x400")

# Кнопка добавления партнёра
add_btn = ttk.Button(root, text="Добавить партнёра", command=open_add_partner_window)
add_btn.pack(pady=10)

# Создание области со скроллингом
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Вложенный фрейм для партнёров
list_frame = ttk.Frame(scrollable_frame)
list_frame.pack(fill="both", expand=True)

# Автоматическая загрузка при запуске
root.after(100, fetch_partners)

root.mainloop()
