import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Change this as needed
        password="yourpassword",  # Change this
        database="erp_system"
    )

# Fetch employee data
def fetch_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM employees WHERE emp_id = %s"
    cursor.execute(query, (emp_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# Show employee data
def show_profile():
    emp_id = entry_id.get()
    if not emp_id.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid numeric ID.")
        return
    
    emp_data = fetch_employee(int(emp_id))
    
    if emp_data:
        label_name_val.config(text=emp_data[1])
        label_dept_val.config(text=emp_data[2])
        label_email_val.config(text=emp_data[3])
        label_phone_val.config(text=emp_data[4])
    else:
        messagebox.showinfo("Not Found", "Employee not found.")

# Tkinter GUI
root = tk.Tk()
root.title("Employee ERP System")
root.geometry("400x300")

tk.Label(root, text="Enter Employee ID:", font=('Arial', 12)).pack(pady=10)
entry_id = tk.Entry(root, font=('Arial', 12))
entry_id.pack()

tk.Button(root, text="View Profile", command=show_profile, font=('Arial', 12)).pack(pady=10)

# Labels to show profile
tk.Label(root, text="Name:", font=('Arial', 10)).pack()
label_name_val = tk.Label(root, text="", font=('Arial', 10))
label_name_val.pack()

tk.Label(root, text="Department:", font=('Arial', 10)).pack()
label_dept_val = tk.Label(root, text="", font=('Arial', 10))
label_dept_val.pack()

tk.Label(root, text="Email:", font=('Arial', 10)).pack()
label_email_val = tk.Label(root, text="", font=('Arial', 10))
label_email_val.pack()

tk.Label(root, text="Phone:", font=('Arial', 10)).pack()
label_phone_val = tk.Label(root, text="", font=('Arial', 10))
label_phone_val.pack()

root.mainloop()