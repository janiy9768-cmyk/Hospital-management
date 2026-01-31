# page_after_login.py
from tkinter import *
from PIL import Image, ImageTk
import os
import AddPatients
import Appoinment_FILE

BASE_DIR = os.path.dirname(__file__)


def page_after_login():
    window = Tk()
    window.title("Hospital Management - Dashboard")

    try:
        window.state("zoomed")
    except:
        window.geometry("1250x720")

    window.configure(bg="#E9F1FA")
    window.resizable(True, True)

    # ---------------------- LOAD BACKGROUND IMAGE ----------------------
    bg_path = os.path.join(BASE_DIR, "Image3.jpg")
    bg = None

    if os.path.exists(bg_path):
        img = Image.open(bg_path)
        img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
        bg = ImageTk.PhotoImage(img)

        bg_label = Label(window, image=bg)
        bg_label.image = bg
        bg_label.place(relwidth=1, relheight=1)

    # ---------------------- TOP NAV BAR ----------------------
    topbar = Frame(window, bg="#1F3C88", height=70)
    topbar.pack(side="top", fill="x")

    Label(
        topbar,
        text="🏥 Hospital Management System",
        bg="#1F3C88",
        fg="white",
        font=("Segoe UI", 22, "bold"),
        padx=20
    ).pack(side="left", pady=10)

    # ---------------------- SIDEBAR ----------------------
    sidebar = Frame(window, bg="#112D4E", width=260)
    sidebar.pack(side="left", fill="y")

    Label(
        sidebar,
        text=" Dashboard",
        bg="#112D4E",
        fg="white",
        font=("Segoe UI", 20, "bold"),
        anchor="w",
        padx=20
    ).pack(pady=40)

    btn_style = {
        "font": ("Segoe UI", 13, "bold"),
        "bg": "#3F72AF",
        "fg": "white",
        "activebackground": "#2E5C92",
        "activeforeground": "white",
        "bd": 0,
        "width": 18,
        "height": 2,
        "cursor": "hand2"
    }

    Button(
        sidebar, text="➕  Add Patient",
        command=lambda: open_add_patient(window), **btn_style
    ).pack(pady=15)

    Button(
        sidebar, text="📅  Book Appointment",
        command=lambda: open_book_appt(window), **btn_style
    ).pack(pady=15)

    Button(
        sidebar, text="🚪  Sign Out",
        command=window.destroy, **btn_style
    ).pack(pady=15)

    # ---------------------- MAIN CONTENT AREA ----------------------
    content = Frame(window, bg="#E9F1FA")
    content.pack(side="left", fill="both", expand=True)

    # Glass panel in center
    glass_panel = Frame(content, bg="white", bd=0, highlightthickness=0)
    glass_panel.place(relx=0.5, rely=0.5, anchor="center", width=700, height=330)

    Label(
        glass_panel,
        text="Welcome to Hospital Management System",
        font=("Segoe UI", 26, "bold"),
        bg="white",
        fg="#1F3C88"
    ).pack(pady=35)

    Label(
        glass_panel,
        text="Select an option from the left panel to continue.",
        font=("Segoe UI", 18),
        bg="white",
        fg="#3F72AF"
    ).pack()

    window.mainloop()


# ------------------- BUTTON ACTIONS -------------------
def open_add_patient(parent_window):
    parent_window.destroy()
    AddPatients.add_patient()


def open_book_appt(parent_window):
    parent_window.destroy()
    Appoinment_FILE.book_appointment()
