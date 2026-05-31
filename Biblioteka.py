# Import necessary libraries
import tkinter as tk  # GUI framework
from tkinter import messagebox, simpledialog, font  # GUI dialog and font utilities
import mysql.connector  # MySQL database connector

# ------------------- DATABASE CONNECTION -------------------

def connect_db():
    # Connect to the MySQL database
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MojasifrazaSQL01_@",
        database="library_db"
    )

# ------------------- GENERAL TABLE DISPLAY FUNCTION -------------------

def fetch_table_data(query):
    # Connect and fetch data from the database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return columns, rows

def open_table_window(title, query):
    # Create a new window to show the result of a table query
    columns, rows = fetch_table_data(query)
    win = tk.Toplevel()
    win.title(title)
    win.geometry("700x400")
    tk.Label(win, text=title, font=("Times New Roman", 20, "bold")).pack(pady=10)
    text_box = tk.Text(win, font=("Times New Roman", 14), wrap="none")
    text_box.pack(fill="both", expand=True, padx=10, pady=10)
    header = " | ".join(columns)
    text_box.insert(tk.END, header + "\n" + "-" * len(header) + "\n")
    for row in rows:
        text_box.insert(tk.END, " | ".join(str(cell) for cell in row) + "\n")

# ------------------- ABOUT LIBRARY STATIC PAGE -------------------

def about_library():
    # Display a static message about the library
    win = tk.Toplevel()
    win.title("About Library")
    win.geometry("600x300")
    tk.Label(win, text="About the Library", font=("Times New Roman", 20, "bold")).pack(pady=10)
    description = (
        "Welcome to the MySQL Library System!\n\n"
        "This library provides a wide collection of books across various genres.\n"
        "Only one librarian manages the system.\n"
        "Members can borrow and return books, while the staff ensures smooth operations.\n"
    )
    tk.Message(win, text=description, font=("Times New Roman", 14), width=550).pack(padx=10, pady=10)

# ------------------- ADD BOOK FUNCTION -------------------

def add_book():
    # Form to add a new book
    win = tk.Toplevel()
    win.title("Add Book")
    win.geometry("500x400")
    labels = ["Book ID", "Name", "Author", "Quantity"]
    entries = []
    tk.Label(win, text="Add New Book", font=("Times New Roman", 18, "bold")).pack(pady=10)
    for label in labels:
        tk.Label(win, text=label, font=("Times New Roman", 14)).pack()
        entry = tk.Entry(win, font=("Times New Roman", 14))
        entry.pack(pady=5)
        entries.append(entry)

    def submit():
        # Get data and insert it into the database
        try:
            book_id = int(entries[0].get())
            name = entries[1].get()
            author = entries[2].get()
            quantity = int(entries[3].get())
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (book_id, name, author, quantity) VALUES (%s, %s, %s, %s)",
                           (book_id, name, author, quantity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book added.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book:\n{e}")

    tk.Button(win, text="Submit", font=("Times New Roman", 14), command=submit).pack(pady=10)

# ------------------- ADD MEMBER FUNCTION -------------------

def add_member():
    # Form to add a new member
    win = tk.Toplevel()
    win.title("Add Member")
    win.geometry("350x300")
    labels = ["Member ID", "Name", "Contact"]
    entries = []
    tk.Label(win, text="Add New Member", font=("Times New Roman", 18, "bold")).pack(pady=10)
    for label in labels:
        tk.Label(win, text=label, font=("Times New Roman", 14)).pack()
        entry = tk.Entry(win, font=("Times New Roman", 14))
        entry.pack(pady=5)
        entries.append(entry)

    def submit():
        # Get data and insert it into the members table
        try:
            member_id = int(entries[0].get())
            name = entries[1].get()
            contact = entries[2].get()
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO members (member_id, name, contact) VALUES (%s, %s, %s)",
                           (member_id, name, contact))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Member added.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add member:\n{e}")

    tk.Button(win, text="Submit", font=("Times New Roman", 14), command=submit).pack(pady=10)

# ------------------- REMOVE BOOK FUNCTION -------------------

def remove_book():
    # Prompt for book ID and remove book from DB
    book_id = simpledialog.askinteger("Remove Book", "Enter Book ID to remove:")
    if book_id:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book removed.")

# ------------------- REMOVE MEMBER FUNCTION -------------------

def remove_member():
    # Prompt for member ID and remove from DB
    member_id = simpledialog.askinteger("Remove Member", "Enter Member ID to remove:")
    if member_id:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Member removed.")

# ------------------- MAIN APPLICATION WINDOW -------------------

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("700x600")  # Larger window size
        self.resizable(False, False)  # Fixed size
        self.configure(bg="navy blue")  # Set background color

        # Fonts for title and buttons
        title_font = font.Font(family="Times New Roman", size=28, weight="bold")
        button_font = font.Font(family="Times New Roman", size=14, weight="bold")

        # Title label
        tk.Label(self, text="MySQL Library", font=title_font, fg="white", bg="navy blue").pack(pady=20)

        # Frame to organize button layout
        button_frame = tk.Frame(self, bg="navy blue")
        button_frame.pack()

        # Button definitions
        buttons = [
            ("SHOW BOOKS", lambda: open_table_window("Books", "SELECT * FROM books")),
            ("SHOW MEMBERS", lambda: open_table_window("Members", "SELECT * FROM members")),
            ("ADD BOOK", add_book),
            ("REMOVE BOOK", remove_book),
            ("ADD MEMBER", add_member),
            ("REMOVE MEMBER", remove_member),
            ("SHOW STAFF", lambda: open_table_window("Staff", "SELECT * FROM staff")),
            ("ABOUT LIBRARY", about_library)
        ]

        # Create a larger grid for buttons with space in the middle
        for i in range(4):
            for j in range(2):
                text, command = buttons[i * 2 + j]
                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=button_font,
                    width=20,
                    height=2,
                    command=command,
                    bg="white",
                    fg="black",
                    relief="raised",
                    bd=3
                )
                btn.grid(row=i, column=j, padx=20, pady=15, ipadx=5, ipady=5)
                btn.config(highlightbackground="white")
                btn.configure(borderwidth=2)
                btn.configure(relief="ridge")
                btn.configure(cursor="hand2")
                btn.configure(highlightthickness=0)
                btn.configure(overrelief="groove")
                btn.configure(relief="groove")
                btn.configure(activebackground="lightblue")
                btn.configure(highlightcolor="lightgray")
                btn.configure(border=0)
                btn.configure(highlightthickness=0)
                btn.configure(font=("Times New Roman", 14, "bold"))
                btn.configure(relief="flat")
                btn.configure(borderwidth=0)
                btn.configure(pady=10)

# ------------------- LAUNCH APPLICATION -------------------

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()