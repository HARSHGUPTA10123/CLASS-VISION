import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
from tkinter import Label, messagebox

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

image_references = []
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# ==================== HELPER FUNCTIONS ====================
def check_enrollment_exists(enrollment_no):
    """Check if enrollment number already exists in student details"""
    if not os.path.exists(studentdetail_path):
        return False
    
    try:
        df = pd.read_csv(studentdetail_path)
        if 'Enrollment' in df.columns:
            return enrollment_no in df['Enrollment'].astype(str).values
    except:
        pass
    return False

def add_student_to_csv(enrollment_no, name):
    """Add new student to CSV file"""
    try:
        if not os.path.exists(studentdetail_path):
            # Create new CSV with headers
            df = pd.DataFrame({'Enrollment': [enrollment_no], 'Name': [name]})
        else:
            # Append to existing CSV
            df = pd.read_csv(studentdetail_path)
            new_student = pd.DataFrame({'Enrollment': [enrollment_no], 'Name': [name]})
            df = pd.concat([df, new_student], ignore_index=True)
        
        df.to_csv(studentdetail_path, index=False)
        return True
    except:
        return False

# ==================== FUNCTIONS DEFINITION ====================
def TakeImageUI():
    ImageUI = Toplevel(window)
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("800x500")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(False, False)
    
    # Center the TakeImage window
    ImageUI.update_idletasks()
    screen_width = ImageUI.winfo_screenwidth()
    screen_height = ImageUI.winfo_screenheight()
    x = (screen_width - 800) // 2
    y = (screen_height - 500) // 2
    ImageUI.geometry(f'800x500+{x}+{y}')
    
    # Title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 25, "bold")
    )
    titl.pack(pady=20)

    # Main frame
    main_frame = Frame(ImageUI, bg="#1c1c1c")
    main_frame.pack(expand=True, fill=BOTH, padx=50, pady=20)

    # ER no
    lbl1 = tk.Label(
        main_frame,
        text="Enrollment No",
        width=12,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 12),
    )
    lbl1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    txt1 = tk.Entry(
        main_frame,
        width=20,
        bd=5,
        validate="key",
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 12),
    )
    txt1.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        main_frame,
        text="Name",
        width=12,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 12),
    )
    lbl2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    txt2 = tk.Entry(
        main_frame,
        width=20,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 12),
    )
    txt2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Notification
    lbl3 = tk.Label(
        main_frame,
        text="Notification",
        width=12,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 12),
    )
    lbl3.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    message = tk.Label(
        main_frame,
        text="",
        width=25,
        height=2,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 10, "bold"),
    )
    message.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    def take_image():
        l1 = txt1.get().strip()
        l2 = txt2.get().strip()
        
        # Validate inputs
        if not l1 or not l2:
            message.config(text="Enrollment & Name required!")
            err_screen()
            return
        
        # Check if enrollment already exists
        if check_enrollment_exists(l1):
            message.config(text="Enrollment already exists!")
            text_to_speech("Enrollment number already used. Please use different enrollment number.")
            return
        
        # Proceed with image capture
        success = takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        
        if success:
            # Add student to CSV only after successful image capture
            if add_student_to_csv(l1, l2):
                message.config(text="Images captured successfully!")
                text_to_speech("Images captured successfully. Now you can train the model.")
            else:
                message.config(text="Error saving student details!")
        else:
            message.config(text="Error capturing images!")

    # Button frame
    button_frame = Frame(ImageUI, bg="#1c1c1c")
    button_frame.pack(pady=30)

    # take Image button
    takeImg = tk.Button(
        button_frame,
        text="Take Image",
        command=take_image,
        bd=8,
        font=("Verdana", 14, "bold"),
        bg="#333333",
        fg="yellow",
        height=1,
        width=12,
        relief=RIDGE,
    )
    takeImg.grid(row=0, column=0, padx=20)

    def train_image():
        # Check if there are any images to train
        if not os.path.exists(trainimage_path) or len(os.listdir(trainimage_path)) == 0:
            message.config(text="No images to train!")
            text_to_speech("No images available for training. Please capture images first.")
            return
        
        # Train the model
        success = trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )
        
        if success:
            message.config(text="Model trained successfully!")
            text_to_speech("Model is trained successfully!")
        else:
            message.config(text="Training failed!")
            text_to_speech("Training failed. Please try again.")

    # train Image function call
    trainImg = tk.Button(
        button_frame,
        text="Train Image",
        command=train_image,
        bd=8,
        font=("Verdana", 14, "bold"),
        bg="#333333",
        fg="yellow",
        height=1,
        width=12,
        relief=RIDGE,
    )
    trainImg.grid(row=0, column=1, padx=20)

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

def del_sc1():
    sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x110")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(False, False)
    
    # Center error window
    sc1.update_idletasks()
    screen_width = sc1.winfo_screenwidth()
    screen_height = sc1.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 110) // 2
    sc1.geometry(f'400x110+{x}+{y}')
    
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack(pady=10)
    
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        font=("Verdana", 14, "bold"),
    ).pack(pady=5)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# ==================== RESPONSIVE FUNCTIONS ====================
def on_window_resize(event):
    # Update fonts and layouts when window is resized
    if event.widget == window:
        update_layout()

def update_layout():
    # Get current window dimensions
    width = window.winfo_width()
    height = window.winfo_height()
    
    # Update fonts based on window size
    title_font_size = max(20, width // 60)
    welcome_font_size = max(16, width // 80)
    button_font_size = max(10, width // 100)
    
    # Update title font
    title_label.config(font=("Verdana", title_font_size, "bold"))
    
    # Update welcome font
    # welcome_label.config(font=("Verdana", welcome_font_size, "bold"))
    
    # Update button fonts
    for frame in [register_frame, verify_frame, attendance_frame]:
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(font=("Verdana", button_font_size, "bold"))

# ==================== MAIN WINDOW SETUP ====================
window = Tk()
window.title("Face Recognizer")
window.configure(background="#1c1c1c")

# Make window resizable instead of fullscreen
window.geometry("1200x800")  # Set initial size
window.resizable(True, True)  # Allow resizing

# Center the window on screen
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - 1200) // 2
y = (screen_height - 800) // 2
window.geometry(f'1200x800+{x}+{y}')

# ==================== TITLE SECTION ====================
# Title frame
title_frame = Frame(window, bg="#1c1c1c", relief=RIDGE, bd=8)
title_frame.pack(fill=X, pady=10)

# Load and display logo
logo = Image.open("UI_Image/0001.png")
logo = logo.resize((50, 50), Image.Resampling.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
image_references.append(logo1)

logo_label = Label(title_frame, image=logo1, bg="#1c1c1c")
logo_label.pack(side=LEFT, padx=20)

title_label = Label(
    title_frame, 
    text="CLASS VISION AI",
    bg="#1c1c1c", 
    fg="yellow", 
    font=("Verdana", 28, "bold")
)
title_label.pack(side=LEFT, padx=10)

# ==================== WELCOME MESSAGE ====================
welcome_label = Label(
    window,
    text="SMART ATTENDANCE SYSTEM",
    bg="#1c1c1c",
    fg="yellow",
    font=("Verdana", 40, "bold"),
)
welcome_label.pack(fill=X,pady=10)

# ==================== MAIN CONTENT FRAME ====================
# Create a main container that expands
main_container = Frame(window, bg="#1c1c1c")
main_container.pack(fill=BOTH, expand=True, padx=40, pady=20)

# Configure grid weights for responsiveness
main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=1)
main_container.grid_columnconfigure(1, weight=1)
main_container.grid_columnconfigure(2, weight=1)

# ==================== IMAGES SECTION ====================
# Register Image
ri = Image.open("UI_Image/register.png")
ri = ri.resize((200, 200), Image.Resampling.LANCZOS)
r = ImageTk.PhotoImage(ri)
image_references.append(r)

register_frame = Frame(main_container, bg="#1c1c1c")
register_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
register_frame.grid_rowconfigure(0, weight=1)
register_frame.grid_rowconfigure(1, weight=0)
register_frame.grid_columnconfigure(0, weight=1)

label1 = Label(register_frame, image=r, bg="#1c1c1c")
label1.grid(row=0, column=0, pady=10)

# Verify Image
vi = Image.open("UI_Image/verifyy.png")
vi = vi.resize((200, 200), Image.Resampling.LANCZOS)
v = ImageTk.PhotoImage(vi)
image_references.append(v)

verify_frame = Frame(main_container, bg="#1c1c1c")
verify_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
verify_frame.grid_rowconfigure(0, weight=1)
verify_frame.grid_rowconfigure(1, weight=0)
verify_frame.grid_columnconfigure(0, weight=1)

label3 = Label(verify_frame, image=v, bg="#1c1c1c")
label3.grid(row=0, column=0, pady=10)

# Attendance Image
ai = Image.open("UI_Image/attendance.png")
ai = ai.resize((200, 200), Image.Resampling.LANCZOS)
a = ImageTk.PhotoImage(ai)
image_references.append(a)

attendance_frame = Frame(main_container, bg="#1c1c1c")
attendance_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
attendance_frame.grid_rowconfigure(0, weight=1)
attendance_frame.grid_rowconfigure(1, weight=0)
attendance_frame.grid_columnconfigure(0, weight=1)

label2 = Label(attendance_frame, image=a, bg="#1c1c1c")
label2.grid(row=0, column=0, pady=10)

# ==================== BUTTONS SECTION ====================
# Register Button
register_btn = tk.Button(
    register_frame,
    text="Register",
    command=TakeImageUI,
    bd=8,
    font=("Verdana", 14, "bold"),
    bg="black",
    fg="yellow",
    height=2,
    width=15,
)
register_btn.grid(row=1, column=0, pady=15)

# Take Attendance Button
attendance_btn = tk.Button(
    verify_frame,
    text="Take Attendance",
    command=automatic_attedance,
    bd=8,
    font=("Verdana", 14, "bold"),
    bg="black",
    fg="yellow",
    height=2,
    width=15,
)
attendance_btn.grid(row=1, column=0, pady=15)

# View Attendance Button
view_btn = tk.Button(
    attendance_frame,
    text="View Attendance",
    command=view_attendance,
    bd=8,
    font=("Verdana", 14, "bold"),
    bg="black",
    fg="yellow",
    height=2,
    width=15,
)
view_btn.grid(row=1, column=0, pady=15)

# ==================== EXIT BUTTON SECTION ====================
exit_frame = Frame(window, bg="#1c1c1c")
exit_frame.pack(side=BOTTOM, pady=20)

exit_btn = tk.Button(
    exit_frame,
    text="EXIT",
    bd=8,
    command=window.quit,
    font=("Verdana", 14, "bold"),
    bg="red",
    fg="white",
    height=1,
    width=12,
)
exit_btn.pack()

# ==================== BIND RESIZE EVENT ====================
window.bind('<Configure>', on_window_resize)

# ==================== START THE APPLICATION ====================
window.mainloop()


