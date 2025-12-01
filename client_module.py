import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------------------
# DATABASE FUNCTIONS
# ---------------------------
def get_connection():
    return sqlite3.connect("zimafa.db")


def add_client_db(name, mobile, email, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (name, mobile, email, address) VALUES (?, ?, ?, ?)",
                (name, mobile, email, address))
    conn.commit()
    conn.close()


def update_client_db(client_id, name, mobile, email, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE clients SET name=?, mobile=?, email=?, address=?
        WHERE id=?
    """, (name, mobile, email, address, client_id))
    conn.commit()
    conn.close()


def delete_client_db(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
    conn.commit()
    conn.close()


def search_clients(keyword):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM clients
        WHERE name LIKE ? OR mobile LIKE ? OR email LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    conn.close()
    return rows


# ---------------------------
# UI – CLIENT WINDOW
# ---------------------------
def open_client_window():
    win = tk.Toplevel()
    win.title("Client Management")
    win.geometry("800x500")

    # ---------------------------
    # INPUT FRAME
    # ---------------------------
    frame = tk.LabelFrame(win, text="Client Details", padx=10, pady=10)
    frame.pack(fill="x", padx=10, pady=10)

    tk.Label(frame, text="Name:").grid(row=0, column=0)
    entry_name = tk.Entry(frame, width=30)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Mobile:").grid(row=1, column=0)
    entry_mobile = tk.Entry(frame, width=30)
    entry_mobile.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Email:").grid(row=2, column=0)
    entry_email = tk.Entry(frame, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Address:").grid(row=3, column=0)
    entry_address = tk.Entry(frame, width=30)
    entry_address.grid(row=3, column=1, padx=5, pady=5)

    # ---------------------------
    # TREEVIEW TABLE
    # ---------------------------
    table = ttk.Treeview(win, columns=("id", "name", "mobile", "email", "address"), show="headings")
    table.heading("id", text="ID")
    table.heading("name", text="Name")
    table.heading("mobile", text="Mobile")
    table.heading("email", text="Email")
    table.heading("address", text="Address")
    table.column("id", width=40)
    table.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------------------
    # FUNCTIONS
    # ---------------------------
    def load_clients():
        table.delete(*table.get_children())
        for row in get_all_clients():
            table.insert("", "end", values=row)

    def add_client():
        name = entry_name.get()
        mobile = entry_mobile.get()
        email = entry_email.get()
        address = entry_address.get()

        if name == "" or mobile == "":
            messagebox.showerror("Error", "Name & Mobile are required!")
            return

        add_client_db(name, mobile, email, address)
        load_clients()
        messagebox.showinfo("Success", "Client Added Successfully")

    def edit_client():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a client to edit")
            return

        row = table.item(selected)["values"]
        client_id = row[0]

        update_client_db(client_id, entry_name.get(), entry_mobile.get(),
                         entry_email.get(), entry_address.get())
        load_clients()
        messagebox.showinfo("Updated", "Client Updated Successfully")

    def delete_client():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a client to delete")
            return

        row = table.item(selected)["values"]
        client_id = row[0]

        delete_client_db(client_id)
        load_clients()
        messagebox.showinfo("Deleted", "Client Deleted Successfully")

    def search():
        keyword = entry_search.get()
        table.delete(*table.get_children())
        for row in search_clients(keyword):
            table.insert("", "end", values=row)

    def select_row(event):
        selected = table.selection()
        if selected:
            row = table.item(selected)["values"]
            entry_name.delete(0, tk.END)
            entry_mobile.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_address.delete(0, tk.END)

            entry_name.insert(0, row[1])
            entry_mobile.insert(0, row[2])
            entry_email.insert(0, row[3])
            entry_address.insert(0, row[4])

    table.bind("<<TreeviewSelect>>", select_row)

    # ---------------------------
    # SEARCH BAR
    # ---------------------------
    search_frame = tk.Frame(win)
    search_frame.pack(pady=5)

    entry_search = tk.Entry(search_frame, width=30)
    entry_search.grid(row=0, column=0, padx=5)

    btn_search = tk.Button(search_frame, text="Search", bg="yellow", command=search)
    btn_search.grid(row=0, column=1)

    # ---------------------------
    # BUTTONS
    # ---------------------------
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Client", width=15, bg="green", fg="white",
              command=add_client).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="Update Client", width=15, bg="blue", fg="white",
              command=edit_client).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="Delete Client", width=15, bg="red", fg="white",
              command=delete_client).grid(row=0, column=2, padx=10)

    tk.Button(btn_frame, text="Refresh", width=15, bg="gray", fg="white",
              command=load_clients).grid(row=0, column=3, padx=10)

    load_clients()

