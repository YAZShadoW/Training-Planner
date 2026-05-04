import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'trainings.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def validate_duration(duration_str):
    try:
        duration = float(duration_str)
        return duration > 0
    except ValueError:
        return False

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Training Planner')
        self.data = load_data()

        # --- Поля ввода ---
        ttk.Label(root, text='Дата (ДД.ММ.ГГГГ):').grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text='Тип тренировки:').grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text='Длительность (мин):').grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        ttk.Button(root, text='Добавить тренировку', command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=('date', 'type', 'duration'), show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип')
        self.tree.heading('duration', text='Длительность')
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # --- Фильтрация ---
        ttk.Label(root, text='Фильтр по типу:').grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Entry(root)
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(root, text='Фильтр по дате:').grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(root, text='Применить фильтр', command=self.apply_filter).grid(row=7, column=0, padx=5, pady=5)
        ttk.Button(root, text='Сбросить фильтр', command=self.reset_filter).grid(row=7, column=1, padx=5, pady=5)

        self.update_table()

    def add_training(self):
        date = self.date_entry.get().strip()
        tr_type = self.type_entry.get().strip()
        duration = self.duration_entry.get().strip()

        if not date or not tr_type or not duration:
            messagebox.showerror('Ошибка', 'Все поля обязательны для заполнения!')
            return

        if not validate_date(date):
            messagebox.showerror('Ошибка', 'Неверный формат даты! Используйте ДД.ММ.ГГГГ')
            return

        if not validate_duration(duration):
            messagebox.showerror('Ошибка', 'Длительность должна быть положительным числом!')
            return

        self.data.append({'date': date, 'type': tr_type, 'duration': float(duration)})
        save_data(self.data)

        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in self.data:
            self.tree.insert('', tk.END, values=(item['date'], item['type'], item['duration']))

    def apply_filter(self):
        f_type = self.filter_type.get().strip().lower()
        f_date = self.filter_date.get().strip()

        filtered = self.data

        if f_type:
            filtered = [x for x in filtered if f_type in x['type'].lower()]

        if f_date and validate_date(f_date):
            filtered = [x for x in filtered if x['date'] == f_date]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in filtered:
            self.tree.insert('', tk.END, values=(item['date'], item['type'], item['duration']))

    def reset_filter(self):
        self.filter_type.delete(0, tk.END)
        self.filter_date.delete(0, tk.END)
        self.update_table()


if __name__ == '__main__':
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
