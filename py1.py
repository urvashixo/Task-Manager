import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
import time

# Initialize an empty dictionary to store tasks grouped by due date
tasks_by_date = {}

# Function to add a task
def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END)
    due_date = due_date_entry.get()
    due_time = due_time_entry.get()
    if title.strip() == "":
        messagebox.showerror("Error", "Please enter a title for the task.")
        return
    tasks_listbox.insert("", tk.END, values=(title, description, due_date, due_time))
    if due_date not in tasks_by_date:
        tasks_by_date[due_date] = []
    tasks_by_date[due_date].append((title, description, due_time))
    clear_entries()
    messagebox.showinfo("Success", "Task added successfully!")

# Function to clear entry fields
def clear_entries():
    title_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)
    due_date_entry.delete(0, tk.END)
    due_time_entry.delete(0, tk.END)

# Function to delete a task
def delete_task():
    selection = tasks_listbox.selection()
    if selection:
        item = tasks_listbox.selection()[0]
        task_data = tasks_listbox.item(item)['values']
        due_date = task_data[2]
        tasks_by_date[due_date].remove((task_data[0], task_data[1], task_data[3]))
        tasks_listbox.delete(item)
        messagebox.showinfo("Success", "Task deleted successfully!")
    else:
        messagebox.showerror("Error", "Please select a task to delete.")

def check_alarms():
  while True:
    current_time = datetime.now()
    already_reminded = set()  # Keep track of tasks already reminded

    for date in tasks_by_date:
      # Check for tasks due today (alarm 15 minutes before)
      if date == current_time.strftime("%Y-%m-%d"):
        for task in tasks_by_date[date]:
          due_time = datetime.strptime(task[2], "%H:%M")
          alarm_time = due_time - timedelta(minutes=15)
          if alarm_time.hour == current_time.hour and alarm_time.minute == current_time.minute:
            messagebox.showinfo("Alarm", f"Task '{task[0]}' is due in 15 minutes!")

      # Check for tasks due tomorrow (reminder shown only once)
      elif date == (current_time + timedelta(days=1)).strftime("%Y-%m-%d"):
        for task in tasks_by_date[date]:
          if task[0] not in already_reminded:  # Check if already reminded
            messagebox.showinfo("Reminder", f"Task '{task[0]}' is due tomorrow!")
            already_reminded.add(task[0])  # Add task to reminded set

      # Handle overdue tasks (same as before)
          elif date < current_time.strftime("%Y-%m-%d"):
                for task in tasks_by_date[date]:
                    item = tasks_listbox.get_children()
                    for i in item:
                        if tasks_listbox.item(i, 'values')[0] == task[0]:
                            tasks_listbox.item(i, tags='overdue')
    time.sleep(60)  # Check every minute       

# Create main window
root = tk.Tk()
root.title("Task Manager")

# Add style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", foreground="white", background="#4CAF50", font=('Helvetica', 10))
style.configure("TLabel", font=('Helvetica', 10))
style.configure("TEntry", font=('Helvetica', 10))
style.configure("TText", font=('Helvetica', 10))

# Create GUI elements with styling
title_label = ttk.Label(root, text="Title:")
title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

title_entry = ttk.Entry(root, width=50)
title_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

description_label = ttk.Label(root, text="Description:")
description_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

description_entry = tk.Text(root, width=50, height=4)
description_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

due_date_label = ttk.Label(root, text="Due Date (YYYY-MM-DD):")
due_date_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

due_date_entry = ttk.Entry(root, width=20)
due_date_entry.grid(row=2, column=1, padx=10, pady=5)

due_time_label = ttk.Label(root, text="Due Time (HH:MM):")
due_time_label.grid(row=2, column=2, sticky="w", padx=10, pady=5)

due_time_entry = ttk.Entry(root, width=10)
due_time_entry.grid(row=2, column=3, padx=10, pady=5)

add_button = ttk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

delete_button = ttk.Button(root, text="Delete Task", command=delete_task)
delete_button.grid(row=3, column=2, columnspan=2, padx=10, pady=5, sticky="we")

tasks_listbox = ttk.Treeview(root, columns=("Title", "Description", "Due Date", "Due Time"), selectmode='browse')
tasks_listbox.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="nswe")
tasks_listbox.heading("#0", text="", anchor="w")
tasks_listbox.heading("Title", text="Title")
tasks_listbox.heading("Description", text="Description")
tasks_listbox.heading("Due Date", text="Due Date")
tasks_listbox.heading("Due Time", text="Due Time")
tasks_listbox.column("#0", width=1, stretch=tk.NO)
tasks_listbox.column("Title", anchor="w", width=150)
tasks_listbox.column("Description", anchor="w", width=200)
tasks_listbox.column("Due Date", anchor="w", width=100)
tasks_listbox.column("Due Time", anchor="w", width=80)
tasks_listbox.tag_configure('overdue', background='red')

# Start the alarm checking thread
alarm_thread = threading.Thread(target=check_alarms, daemon=True)
alarm_thread.start()

# Configure grid weights to make the listbox expandable
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(4, weight=1)

# Main loop
root.mainloop()
