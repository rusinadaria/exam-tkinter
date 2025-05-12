import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://localhost:8080/api/partners"

def fetch_partners():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        partners = response.json()
        listbox.delete(0, tk.END)
        for partner in partners:
            listbox.insert(tk.END, partner)
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные:\n{e}")

# Создание окна
root = tk.Tk()
root.title("Список партнёров")
root.geometry("400x300")



# 2

# Список для отображения партнёров
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Автоматическая загрузка данных при открытии окна
root.after(100, fetch_partners)

# Запуск главного цикла
root.mainloop()


# 1

# # Кнопка для загрузки партнёров
# btn_fetch = ttk.Button(root, text="Загрузить партнёров", command=fetch_partners)
# btn_fetch.pack(pady=10)

# # Список для отображения партнёров
# listbox = tk.Listbox(root, width=50, height=10)
# listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# # Запуск главного цикла
# root.mainloop()
