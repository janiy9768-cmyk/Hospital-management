# Appoinment_FILE.py
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
import os
import datetime
import page_after_login as pal

BASE_DIR = os.path.dirname(__file__)

# ------------------ MYSQL CONNECTION ------------------
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
        messagebox.showerror("DB Error", f"Cannot connect to MySQL:\n{e}")
        return None


# ------------------ ENSURE TABLE ------------------
def ensure_tables():
    conn = connect_db()
    if conn is None:
        return

    cur = None
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_name VARCHAR(255) NOT NULL,
                contact VARCHAR(100),
                appt_date DATE NOT NULL,
                notes TEXT
            )
        """)
    except Exception as e:
        messagebox.showerror("Database Error", f"Error creating appointment table:\n{e}")
    finally:
        if cur:
            try: cur.close()
            except: pass
        try:
            conn.close()
        except: pass


# ------------------ BOOK APPOINTMENT WINDOW ------------------
def book_appointment():
    ensure_tables()

    win = Tk()
    win.title("Book Appointment")

    try:
        win.state("zoomed")
    except:
        pass

    win.resizable(True, True)

    # Close window behavior
    def on_close():
        try:
            win.destroy()
        except:
            pass
        try:
            pal.page_after_login()
        except:
            pass

    win.protocol("WM_DELETE_WINDOW", on_close)

    # ----- Background Image (UPDATED TO Image2.jpg) -----
    bg_path = os.path.join(BASE_DIR, "Image2.jpg")

    if os.path.exists(bg_path):
        try:
            sw = win.winfo_screenwidth()
            sh = win.winfo_screenheight()
            img = Image.open(bg_path).resize((sw, sh), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(img)

            bg_label = Label(win, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Background load error:", e)
    else:
        print("Background image not found:", bg_path)

    # ----- Appointment Form Container -----
    card = Frame(win, bg="white", bd=0, relief=SOLID)
    card.place(relx=0.5, rely=0.5, anchor="center", width=550, height=520)

    # Header
    header = Frame(card, bg="#005A9E", height=70)
    header.pack(fill=X)

    Label(header, text=" Book Appointment",
          font=("Arial", 20, "bold"),
          bg="#005A9E", fg="white").pack(pady=15)

    # Form Body
    form = Frame(card, bg="white")
    form.pack(pady=20)

    name_var = StringVar()
    contact_var = StringVar()
    date_var = StringVar(value=str(datetime.date.today()))
    notes_var = StringVar()

    # Add form field function
    def add_field(text, variable):
        Label(form, text=text, bg="white", anchor="w",
              font=("Arial", 12, "bold")).pack(fill=X, padx=40, pady=(10, 0))
        Entry(form, textvariable=variable,
              font=("Arial", 12), bd=1, relief=SOLID,
              highlightbackground="#999",
              highlightcolor="#005A9E",
              highlightthickness=1).pack(fill=X, padx=40, ipady=5)

    add_field("Patient Name", name_var)
    add_field("Contact Number", contact_var)
    add_field("Appointment Date (YYYY-MM-DD)", date_var)
    add_field("Notes", notes_var)

    # -------- SAVE APPOINTMENT ---------
    def save_appt():
        name = name_var.get().strip()
        contact = contact_var.get().strip()
        appt_date = date_var.get().strip()
        notes = notes_var.get().strip()

        if not name:
            messagebox.showwarning("Validation Error", "Patient name is required.")
            return

        # Validate date format
        try:
            datetime.date.fromisoformat(appt_date)
        except:
            messagebox.showwarning("Validation Error", "Invalid date format (YYYY-MM-DD).")
            return

        conn = connect_db()
        if conn is None:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO appointments (patient_name, contact, appt_date, notes)
                VALUES (%s, %s, %s, %s)
            """, (name, contact, appt_date, notes))

            messagebox.showinfo("Success", "Appointment booked successfully!")

            try: win.destroy()
            except: pass
            try: pal.page_after_login()
            except: pass

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save appointment:\n{e}")
        finally:
            try: cur.close()
            except: pass
            try: conn.close()
            except: pass

    # -------- BUTTONS ---------
    btn_frame = Frame(card, bg="white")
    btn_frame.pack(pady=20)

    Button(btn_frame, text="Book Appointment",
           width=18, height=2,
           font=("Arial", 12, "bold"),
           bg="#0078D4", fg="white",
           cursor="hand2",
           command=save_appt).grid(row=0, column=0, padx=10)

    Button(btn_frame, text="Cancel",
           width=18, height=2,
           font=("Arial", 12, "bold"),
           bg="#E0E0E0",
           cursor="hand2",
           command=on_close).grid(row=0, column=1, padx=10)


# -------- RUN PAGE --------
if __name__ == "__main__":
    book_appointment()
