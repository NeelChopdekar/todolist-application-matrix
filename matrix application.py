import tkinter as tk
from tkinter import ttk, messagebox


import sqlite3

#CREATING THE DATABASE USING SQLITE3
connect = sqlite3.connect("tasks.db")
cursor = connect.cursor()   
cursor.execute(" CREATE TABLE IF NOT EXISTS tasks ( id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, priority TEXT ) ")
connect.commit()


def load_tasks():
    for task in task_list.get_children():     #Load_tasks function to prevent duplication of tasks by deleting all the previous tasks.
        task_list.delete(task)
    e = cursor.execute("SELECT * FROM tasks")
    for row in e:
        task_list.insert("", "end", values=row)

def add_task():                              #Function to add tasks to the database and UI.
    task = task_entry.get()
    priority = priority_var.get()
    if len(task) == 0:
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return
    cursor.execute("INSERT INTO tasks (task, priority) VALUES (?, ?)", (task, priority))
    connect.commit()
    task_entry.delete(0, tk.END)
    load_tasks()

def delete_task():                           #Deletes the selected task
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a task to delete!")
        return
    task_id = task_list.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connect.commit()
    load_tasks()



dark_mode = False

def dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    style = ttk.Style()

    if dark_mode:
        root.config(bg="#1C1C1E")
        title_label.config(bg="#1C1C1E", fg="white")
        task_entry.config(bg="#2C2C2E", fg="white", insertbackground="white")
        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=25)
        style.map("Treeview", background=[("selected", "#444444")], foreground=[("selected", "white")])

    else:
        root.config(bg="#F5F5F5")
        title_label.config(bg="#F5F5F5", fg="black")
        task_entry.config(bg="white", fg="black", insertbackground="black")
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", rowheight=25)
        style.map("Treeview", background=[("selected", "#87CEEB")], foreground=[("selected", "black")])



root = tk.Tk()
root.title("To-Do List")
root.geometry("500x600")
root.config(bg="#F5F5F5")

title_label = tk.Label(root, text="ToDo List", font=("Ariel", 30, "bold"), fg="black", bg="#F5F5F5")
title_label.pack(pady=10)

task_entry = tk.Entry(root, font=("Ariel", 12), width=35)
task_entry.pack(pady=10)

priority_var=tk.StringVar(value="Low")
priority_dropdown = ttk.Combobox(root, values=["Low", "Medium", "High"], font=("Ariel", 12))
priority_dropdown.pack()


button_frame = tk.Frame(root, bg="#F5F5F5")
button_frame.pack(pady=10)

def create_button(text, command):               #Function to create buttons to add/delete tasks
    button = tk.Button(button_frame, text=text, command=command, font=("Ariel", 12), bg="#9E3B2E", fg="WHITE", bd=0, width=12)
    button.grid(row=1, column=button_frame.grid_size()[0])
    return button

create_button("Add Task", add_task)   #Creates button to add tasks
create_button("Delete Task", delete_task)  #Creates button to delete tasks


columns = ("ID", "Task", "Priority")
task_list = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse", height=10)
style = ttk.Style()
style.configure("Treeview", background="#333333", foreground="white", rowheight=25)  
style.map("Treeview", background=[("selected", "#444444")], foreground=[("selected", "white")])

task_list.heading("ID", text="ID")
task_list.heading("Task", text="Task")
task_list.heading("Priority", text="Priority")
task_list.column("ID", width=50)
task_list.column("Task", width=300)
task_list.column("Priority", width=150)
task_list.pack(pady=10, fill="both", expand=True)

# Dark Mode Toggle
dark_mode_button = tk.Button(root, text="Toggle Dark Mode", command=dark_mode, font=("Ariel", 12), bg="#9E3B2E", fg="WHITE")
dark_mode_button.pack(pady=10)


load_tasks()

root.mainloop()

