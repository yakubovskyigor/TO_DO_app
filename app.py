import tkinter as tk

from pymongo import MongoClient
from tkinter import messagebox, simpledialog
from tkinter import ttk


client = MongoClient("mongodb://localhost:27017/")
db = client["todo_app"]
collection = db["todo"]


def add_task():
    task_text = entry.get()
    if task_text:
        task = {"text": task_text}
        collection.insert_one(task)
        listbox.insert(tk.END, task_text)
        entry.delete(0, tk.END)


def delete_task():
    selected_index = listbox.curselection()
    if selected_index:
        selected_task = listbox.get(selected_index[0])
        task_text = selected_task
        result = messagebox.askquestion(
            "Deleting a task",
            f"Are you sure you want to delete the task: {task_text}?",
            icon="warning",
        )
        if result == "yes":
            collection.delete_one({"text": task_text})
            listbox.delete(selected_index[0])


def edit_task():
    selected_index = listbox.curselection()
    if selected_index:
        selected_task = listbox.get(selected_index[0])
        new_text = simpledialog.askstring(
            "Edit task", "Enter a new task text:", initialvalue=selected_task
        )
        if new_text:
            collection.update_one({"text": selected_task}, {"$set": {"text": new_text}})
            listbox.delete(selected_index[0])
            listbox.insert(selected_index[0], new_text)


root = tk.Tk()
root.geometry("700x450+300+100")
root.config(bg="#000000")

label = ttk.Label(
    text="Daily Tasks", font=("Arial", 20), background="#000000", foreground="#FFFFFF"
)
label.pack()

style = ttk.Style()
style.configure("TFrame", background="#292b2a")

frame = ttk.Frame(root)

entry = tk.Entry(frame, width=90, bg="#292b2a", foreground="#FFFFFF")
entry.pack(anchor=tk.NW, padx=6, pady=6)

listbox = tk.Listbox(frame)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox["yscrollcommand"] = scrollbar.set

frame.pack(padx=125, pady=20)

btn = tk.Button(text="Add", bg="#00008B", foreground="#FFFFFF", command=add_task)
btn.place(relx=0.5, rely=0.7, anchor="center", width=450, height=30)

btn2 = tk.Button(text="Delete", bg="#00008B", foreground="#FFFFFF", command=delete_task)
btn2.place(relx=0.5, rely=0.8, anchor="center", width=450, height=30)

btn_edit = tk.Button(text="Edit", bg="#00008B", foreground="#FFFFFF", command=edit_task)
btn_edit.place(relx=0.5, rely=0.9, anchor="center", width=450, height=30)

root.mainloop()
