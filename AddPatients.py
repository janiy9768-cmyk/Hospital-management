# AddPatients.py
from tkinter import *
from tkinter import messagebox
import os
import pymysql
from PIL import Image, ImageTk
import page_after_login as pal

BASE_DIR = os.path.dirname(__file__)


# -------------------- DB CONNECTION --------------------
def connect_db():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="yash6385",
            database="hospital",
            autocommit=True
        )
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None


# -------------------- CREATE TABLE --------------------
def ensure_tables():
    try:
        conn = connect_db()
        if conn is None:
            return

        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                gender VARCHAR(20),
                contact VARCHAR(100)
            )
        """)
        conn.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))


# -------------------- ADD PATIENT UI --------------------
def add_patient():
    ensure_tables()

    win = Tk()
    win.title("Add Patient")
    win.state("zoomed")

    # -------- Background --------
    bg_path = os.path.join(BASE_DIR, "Image1.jpg")
    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        img = img.resize((win.winfo_screenwidth(), win.winfo_screenheight()))
        bg = ImageTk.PhotoImage(img)

        Label(win, image=bg).place(relwidth=1, relheight=1)

    # -------- Card Frame (New Design) --------
    card = Frame(
        win,
        bg="white",
        bd=0,
        highlightbackground="#d9d9d9",
        highlightthickness=2
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=650, height=550)

    # Title
    Label(
        card,
        text="Add Patient Details",
        bg="white",
        fg="#00ecdb",
        font=("Segoe UI", 26, "bold")
    ).pack(pady=(25, 5))

    Label(
        card,
        text="Enter patient information below",
        bg="white",
        fg="#444",
        font=("Segoe UI", 11)
    ).pack()

    # -------- Variables --------
    name_var = StringVar()
    age_var = StringVar()
    gender_var = StringVar(value="Male")
    contact_var = StringVar()

    # -------- Field Creator --------
    def create_field(label, var, is_option=False):
        field_frame = Frame(card, bg="white")
        field_frame.pack(fill="x", padx=60, pady=10)

        Label(
            field_frame,
            text=label,
            bg="white",
            fg="#222",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        if is_option:
            OptionMenu(field_frame, var, "Male", "Female", "Other").pack(
                fill="x", pady=5
            )
        else:
            Entry(
                field_frame,
                textvariable=var,
                font=("Segoe UI", 12),
                bd=1,
                relief="solid"
            ).pack(fill="x", pady=5)

    # -------- Form Fields --------
    create_field("Full Name", name_var)
    create_field("Age", age_var)
    create_field("Gender", gender_var, is_option=True)
    create_field("Contact Number", contact_var)

    # -------- SAVE LOGIC --------
    def save():
        name = name_var.get().strip()
        age = age_var.get().strip()
        gender = gender_var.get().strip()
        contact = contact_var.get().strip()

        if not name:
            messagebox.showwarning("Error", "Full Name is required!")
            return

        if age and not age.isnumeric():
            messagebox.showwarning("Error", "Age must be numeric!")
            return

        if age == "":
            age = None

        try:
            conn = connect_db()
            if conn is None:
                return

            cur = conn.cursor()
            cur.execute("""
                INSERT INTO patients (name, age, gender, contact)
                VALUES (%s, %s, %s, %s)
            """, (name, age, gender, contact))
            conn.close()

            messagebox.showinfo("Success", "Patient Added Successfully!")
            win.destroy()
            pal.page_after_login()

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # -------- Buttons --------
    button_frame = Frame(card, bg="white")
    button_frame.pack(pady=30, padx=60, fill="x")

    Button(
        button_frame,
        text="Save",
        bg="#1A73E8",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        height=2,
        relief="flat",
        command=save
    ).pack(side="left", expand=True, fill="x", padx=(0, 10))

    Button(
        button_frame,
        text="Cancel",
        bg="#cccccc",
        fg="#333",
        font=("Segoe UI", 13, "bold"),
        height=2,
        relief="flat",
        command=lambda: (win.destroy(), pal.page_after_login())
    ).pack(side="left", expand=True, fill="x", padx=(10, 0))

    win.mainloop()


if __name__ == "__main__":
    add_patient()
