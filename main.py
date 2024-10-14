import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import re
import hashlib
from datetime import datetime
import database as db

# Create the database if it doesn't exist
db.create_tables()

# Helper functions
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_password(password):
    return 8 <= len(password) <= 16

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Login and Register functions
def check_login():
    email = email_entry.get().strip()
    password = pw_entry.get().strip()

    if not is_valid_email(email):
        messagebox.showerror("Error", "Please enter a valid email.")
        return
    if not is_valid_password(password):
        messagebox.showerror("Error", "Password must be 8-16 characters.")
        return

    hashed_pw = hash_password(password)

    # Check if the account exists in the database
    try:
        user = db.fetch_account(email, hashed_pw)
        if user is None:
            messagebox.showerror("Error", "Account doesn't exist. Please register.")
        else:
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()  # Close login window
            feedback_window(email)  # Open feedback window
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def check_register():
    email = email_entry.get().strip()
    password = pw_entry.get().strip()

    if not is_valid_email(email):
        messagebox.showerror("Error", "Please enter a valid email.")
        return
    if not is_valid_password(password):
        messagebox.showerror("Error", "Password must be 8-16 characters.")
        return

    hashed_pw = hash_password(password)

    # Register the user in the database
    try:
        if db.fetch_account_by_email(email):
            messagebox.showerror("Error", "Email already exists. Use another email.")
        else:
            db.insert_account(email, hashed_pw)
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Feedback window after login
def feedback_window(email):
    def submit_feedback():
        comment = comment_entry.get().strip()
        if not comment:
            messagebox.showwarning("Input Error", "Please enter a comment.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.insert_comment(email, now, comment)
        comment_entry.delete(0, tk.END)
        refresh_treeview()

    def refresh_treeview():
        for row in tree.get_children():
            tree.delete(row)
        
        feedback_data = pd.DataFrame(db.fetch_feedback(), columns=["CommentID", "Email", "Time", "Comment", "Like"])
        for _, row in feedback_data.iterrows():
            tree.insert("", "end", values=list(row))

    def like_comment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a comment to like.")
            return

        item = selected_item[0]
        print(item)
        current_values = tree.item(item, "values")
        print(current_values)
        comment_id = int(current_values[0])
        print(comment_id)
        liked_comments = db.fetch_record_liked_comments(email)
        if liked_comments and str(comment_id) not in liked_comments.split(","):
            result = db.update_liked_comment(comment_id, email)
            if result == "Already Liked":
                messagebox.showinfo("Info", "You've already liked this comment.")
            else:
                refresh_treeview()
        else:
            messagebox.showinfo("Info", "You've already liked this comment.")


    # Feedback window layout
    feedback_win = tk.Tk()
    feedback_win.title("Feedback Collector")

    # UI elements
    email_label = tk.Label(feedback_win, text=f"Logged in as: {email}")
    comment_label = tk.Label(feedback_win, text="Comment:")
    comment_entry = tk.Entry(feedback_win)
    submit_btn = tk.Button(feedback_win, text="Submit", command=submit_feedback)
    like_btn = tk.Button(feedback_win, text="Like Comment", command=like_comment)

    # Treeview for displaying feedback
    columns = ("CommentID", "Email", "Time", "Comment", "Like")
    tree = ttk.Treeview(feedback_win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    
    refresh_treeview()

    # Layout
    email_label.grid(row=0, column=0, padx=10, pady=10)
    comment_label.grid(row=1, column=0, padx=10, pady=10)
    comment_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="we")
    submit_btn.grid(row=1, column=3, padx=10, pady=10)
    like_btn.grid(row=3, column=2, padx=10, pady=10)
    tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    feedback_win.grid_rowconfigure(2, weight=1)
    feedback_win.grid_columnconfigure(1, weight=1)

    feedback_win.mainloop()

# Tkinter login window setup
root = tk.Tk()
root.geometry('300x350')
root.title('Login')

# UI elements for login
login_label = tk.Label(root, text="Login")
email_label = tk.Label(root, text="Email:")
pw_label = tk.Label(root, text="Password:")

email_entry = tk.Entry(root)
pw_entry = tk.Entry(root, show='*')

login_btn = tk.Button(root, text='Login', command=check_login)
register_btn = tk.Button(root, text='Register', command=check_register)

# Layout for login window
login_label.grid(row=0, column=1, columnspan=2, pady=20)
email_label.grid(row=1, column=0, padx=30)
pw_label.grid(row=2, column=0)
email_entry.grid(row=1, column=1, columnspan=2)
pw_entry.grid(row=2, column=1, columnspan=2)
login_btn.grid(row=3, column=1)
register_btn.grid(row=3, column=2)

root.mainloop()
