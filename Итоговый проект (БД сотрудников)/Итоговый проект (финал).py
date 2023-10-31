import tkinter as tk
from tkinter import ttk
import sqlite3

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список сотрудников компании")
        
        # Подключение к базе данных SQLite и создание курсора
        self.conn = sqlite3.connect("employees.db")
        self.cursor = self.conn.cursor()
        
        # Создание таблицы, если она не существует
        self.create_table()
        
        # Создание элементов пользовательского интерфейса
        self.create_widgets()
        
        # Заполнение Treeview данными из базы данных
        self.populate_treeview()
    
    def create_table(self):
        # Создание таблицы employees с полями id, full_name, phone_number, email, salary
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                phone_number TEXT,
                email TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    def create_widgets(self):
        # Создание Treeview для отображения данных
        self.tree = ttk.Treeview(self.root, columns=("ID", "Full Name", "Phone Number", "Email", "Salary"))
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Full Name")
        self.tree.heading("#3", text="Phone Number")
        self.tree.heading("#4", text="Email")
        self.tree.heading("#5", text="Salary")
        self.tree.pack()
        
        # Создание кнопок для управления данными
        add_button = tk.Button(self.root, text="Добавить сотрудника", command=self.add_employee)
        update_button = tk.Button(self.root, text="Изменить сотрудника", command=self.update_employee)
        delete_button = tk.Button(self.root, text="Удалить сотрудника", command=self.delete_employee)
        search_button = tk.Button(self.root, text="Поиск по ФИО", command=self.search_employee)
        
        add_button.pack()
        update_button.pack()
        delete_button.pack()
        search_button.pack()
    
    def populate_treeview(self):
        # Очистка Treeview и заполнение его данными из базы данных
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM employees")
        employees = self.cursor.fetchall()
        for employee in employees:
            self.tree.insert("", "end", values=employee)
    
    def add_employee(self):
        # Пример добавления сотрудника в базу данных
        new_employee = (
            "Иван Иванович",
            "+79855235145",
            "ivanchik@email.com",
            50000.00
        )
        self.cursor.execute("INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)", new_employee)
        self.conn.commit()
        self.populate_treeview()
    
    def update_employee(self):
        # Пример обновления данных о сотруднике
        self.cursor.execute("UPDATE employees SET salary = ? WHERE id = ?", (55000.00, 1))
        self.conn.commit()
        self.populate_treeview()
    
    def delete_employee(self):
        # Пример удаления сотрудника из базы данных
        self.cursor.execute("DELETE FROM employees WHERE id = ?", (1,))
        self.conn.commit()
        self.populate_treeview()
    
    def search_employee(self):
        # Пример поиска сотрудника по ФИО и отображения результатов в Treeview
        self.tree.delete(*self.tree.get_children())
        search_name = "John Doe"
        self.cursor.execute("SELECT * FROM employees WHERE full_name = ?", (search_name,))
        employees = self.cursor.fetchall()
        for employee in employees:
            self.tree.insert("", "end", values=employee)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()