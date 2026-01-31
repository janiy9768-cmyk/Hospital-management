from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pymysql
import page_after_login

BASE_DIR = os.path.dirname(__file__)


# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    """Return a pymysql connection. Raises exception if can't connect."""
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="yash6385",
            database="hospital",
            autocommit=True
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error",
                             f"Could not connect to MySQL: {e}")
        raise


# ---------------- CREATE USERS TABLE IF MISSING ----------------
def ensure_tables():
    """Create users table and ensure there is a default admin user."""
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
        """)
        cur.execute("SELECT COUNT(*) FROM users")
        cnt = cur.fetchone()[0]

        if cnt == 0:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                        ("admin", "admin"))
        cur.close()

    finally:
        conn.close()


# ---------------- LOGIN PAGE CLASS ----------------
class LoginPage:
    def __init__(self, window):
        self.window = window
        window.title("Hospital Management - Login")
        window.state("zoomed")
        window.minsize(800, 500)

        # ---------- Left Image Panel ----------
        left = Frame(window, width=700)
        left.pack(side=LEFT, fill=Y)

        img_path = os.path.join(BASE_DIR, "Image.jpg")

        if os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((700, window.winfo_screenheight()), Image.LANCZOS)
                self.left_img = ImageTk.PhotoImage(img)
                lbl = Label(left, image=self.left_img)
                lbl.pack(fill=BOTH, expand=True)
            except Exception as e:
                print("Could not load image:", e)
        else:
            print("Image not found:", img_path)

        # ---------- Right Login Panel ----------
        right = Frame(window, bg="#1ff2e1")
        right.pack(side=RIGHT, fill=BOTH, expand=True)

        card = Frame(right, bg="white", bd=2, relief="groove")
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=370)

        Label(card, text="HOSPITAL LOGIN",
              font=("Arial", 18, "bold"), bg="white").pack(pady=16)

        self.user = StringVar()
        self.pwd = StringVar()

        Label(card, text="USER NAME",
              font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        Entry(card, textvariable=self.user, bd=2,
              font=("Arial", 12)).pack(pady=8, ipadx=4, ipady=6)
        Label(card, text="PASSWORD",
              font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        Entry(card, textvariable=self.pwd, bd=2, font=("Arial", 12),
              show="*").pack(pady=8, ipadx=4, ipady=6)

        btn_frame = Frame(card, bg="white")
        btn_frame.pack(pady=12)

        Button(btn_frame, text="Login", width=12,
               bg="#0078D7", fg="white",
               command=self.login).grid(row=0, column=0, padx=8)

        Button(btn_frame, text="Quit", width=10,
               command=window.destroy).grid(row=0, column=1, padx=8)

    # ---------------- LOGIN FUNCTION ----------------
    def login(self):
        u = self.user.get().strip()
        p = self.pwd.get().strip()

        if not u or not p:
            messagebox.showwarning("Validation", "Please enter username and password")
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username=%s", (u,))
            row = cur.fetchone()
            cur.close()
            conn.close()
        except:
            return  # DB error already shown

        if row and row[0] == p:
            self.window.destroy()
            try:
                page_after_login.page_after_login()
            except Exception as e:
                messagebox.showerror("Error",
                                     f"Could not open dashboard: {e}")
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")


# ---------------- START PAGE ----------------
def page():
    try:
        ensure_tables()
    except Exception as e:
        print("ensure_tables failed:", e)

    win = Tk()
    LoginPage(win)
    win.mainloop()


if __name__ == "__main__":
    page()
