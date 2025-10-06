import tkinter as tk
from tkinter import ttk
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import csv

def create_face_recognizer():
    """Create face recognizer with multiple fallback methods"""
    try:
        # Method 1: Try standard opencv-contrib-python installation
        recognizer = cv2.face.LBPHFaceRecognizer.create()
        print("✓ Face recognizer created using cv2.face")
        return recognizer
    except AttributeError:
        print("✗ cv2.face not available, trying alternatives...")
    
    try:
        # Method 2: Try alternative import
        import cv2.face as face
        recognizer = cv2.face.LBPHFaceRecognizer.create()
        print("✓ Face recognizer created using cv2.face import")
        return recognizer
    except (ImportError, AttributeError):
        print("✗ Alternative import failed")
    
    try:
        # Method 3: Try using the base OpenCV (some versions have it differently)
        recognizer = cv2.face.LBPHFaceRecognizer.create()
        print("✓ Face recognizer created using create() method")
        return recognizer
    except AttributeError:
        print("✗ All OpenCV methods failed, using alternative approach")
    
    # Method 4: Use a different face recognition method or show error
    print("⚠ OpenCV face module not available. Please install: pip install opencv-contrib-python")
    return None

# Path configurations
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

# Get the base directory of your project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Project directory: {BASE_DIR}")

# Path configurations with absolute paths
haarcasecade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(BASE_DIR, "TrainingImageLabel", "Trainner.yml")
trainimage_path = os.path.join(BASE_DIR, "TrainingImage")
studentdetail_path = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")
attendance_path = os.path.join(BASE_DIR, "Attendance")

print("All paths configured:")
print(f"Haar Cascade: {haarcasecade_path}")
print(f"Model: {trainimagelabel_path}")
print(f"Training Images: {trainimage_path}")
print(f"Student Details: {studentdetail_path}")
print(f"Attendance: {attendance_path}")

def subjectChoose(text_to_speech):
    
    def FillAttendance():
        sub = tx.get().strip()
        now = time.time()
        future = now + 20
        
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return
        
        # Create face recognizer
        recognizer = create_face_recognizer()
        if recognizer is None:
            error_msg = "Face recognition not available. Please install: pip install opencv-contrib-python"
            Notifica.configure(
                text=error_msg,
                bg="red",
                fg="white",
                width=40,
                font=("times", 12, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech("Face recognition system error")
            return
        
        # Check if model file exists
        if not os.path.exists(trainimagelabel_path):
            error_msg = "Model not found. Please train the model first."
            Notifica.configure(
                text=error_msg,
                bg="black",
                fg="yellow",
                width=33,
                font=("times", 15, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech("Model not found. Please train model first.")
            return
        
        try:
            recognizer.read(trainimagelabel_path)
            print("✓ Model loaded successfully")
        except Exception as e:
            error_msg = f"Error loading model: {str(e)}"
            Notifica.configure(
                text=error_msg,
                bg="black",
                fg="yellow",
                width=33,
                font=("times", 15, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech("Error loading model")
            return
        
        # Load face cascade
        if not os.path.exists(haarcasecade_path):
            error_msg = "Haar cascade file not found."
            Notifica.configure(text=error_msg, bg="red", fg="white")
            Notifica.place(x=20, y=250)
            text_to_speech("Face detection file missing")
            return
        
        face_cascade = cv2.CascadeClassifier(haarcasecade_path)
        
        # Load student details
        if not os.path.exists(studentdetail_path):
            error_msg = "Student details file not found."
            Notifica.configure(text=error_msg, bg="red", fg="white")
            Notifica.place(x=20, y=250)
            text_to_speech("Student details file missing")
            return
        
        df = pd.read_csv(studentdetail_path)
        
        # Initialize camera
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            error_msg = "Cannot open camera. Please check camera connection."
            Notifica.configure(text=error_msg, bg="red", fg="white")
            Notifica.place(x=20, y=250)
            text_to_speech("Camera not available")
            return
        
        font_style = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        
        print("Starting face recognition...")
        
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to capture frame")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                
                try:
                    id_val, confidence = recognizer.predict(roi_gray)
                    
                    # DEBUG: Print prediction details
                    print(f"DEBUG - Predicted ID: {id_val}, Confidence: {confidence}")
                    
                    if confidence < 70:
                        # Check if ID exists in CSV
                        print(f"DEBUG - Looking for ID {id_val} in CSV...")
                        print(f"DEBUG - Available IDs in CSV: {df['Enrollment'].tolist()}")
                        
                        student_info = df[df["Enrollment"] == id_val]
                        
                        if not student_info.empty:
                            student_name = student_info["Name"].values[0]
                            print(f"DEBUG - FOUND: ID {id_val} = {student_name}")
                        else:
                            student_name = "Unknown"
                            print(f"DEBUG - NOT FOUND: ID {id_val} not in CSV")
                        
                        display_text = f"{id_val}-{student_name}"
                        
                        # Add to attendance
                        if id_val not in attendance["Enrollment"].values:
                            attendance.loc[len(attendance)] = [id_val, student_name]
                            print(f"DEBUG - Added to attendance: {id_val}-{student_name}")
                        
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, display_text, (x, y-10), font_style, 0.8, (0, 255, 0), 2)
                    else:
                        # Unknown face
                        display_text = "Unknown"
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(frame, display_text, (x, y-10), font_style, 0.8, (0, 0, 255), 2)
                        print(f"DEBUG - Low confidence: {confidence} (threshold: 70)")
                        
                except Exception as e:
                    print(f"Error in face prediction: {e}")
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, "Error", (x, y-10), font_style, 0.8, (255, 0, 0), 2)
            
            # Show frame
            cv2.imshow("Attendance System - Press ESC to exit", frame)
            
            # Check for timeout or ESC key
            if time.time() > future:
                break
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break

        
        # Release camera and close windows
        cam.release()
        cv2.destroyAllWindows()
        
        # Save attendance if any records found
        if len(attendance) > 0:
            attendance = attendance.drop_duplicates(subset=["Enrollment"], keep="first")
            
            # Create directory if it doesn't exist
            subject_path = os.path.join(attendance_path, sub)
            os.makedirs(subject_path, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{sub}_{timestamp}.csv"
            filepath = os.path.join(subject_path, filename)
            
            attendance.to_csv(filepath, index=False)
            
            success_msg = f"Attendance filled successfully for {sub}. Total: {len(attendance)} students"
            Notifica.configure(
                text=success_msg,
                bg="green",
                fg="white",
                width=40,
                font=("times", 12, "bold"),
            )
            text_to_speech(f"Attendance filled successfully for {sub}")
            
            # Show attendance in new window
            show_attendance_window(attendance, sub)
        else:
            no_face_msg = "No faces recognized for attendance"
            Notifica.configure(
                text=no_face_msg,
                bg="orange",
                fg="black",
                width=33,
                font=("times", 15, "bold"),
            )
            text_to_speech("No faces recognized")
        
        Notifica.place(x=20, y=250)
    
    def show_attendance_window(attendance_df, subject):
        """Display attendance in a new window"""
        window = tk.Toplevel()
        window.title(f"Attendance - {subject}")
        window.geometry("600x400")
        window.configure(bg="white")
        
        title_label = tk.Label(
            window,
            text=f"Attendance for {subject}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="blue"
        )
        title_label.pack(pady=10)
        
        # Create treeview
        tree = ttk.Treeview(window, columns=("Enrollment", "Name"), show="headings")
        tree.heading("Enrollment", text="Enrollment")
        tree.heading("Name", text="Name")
        
        # Add data
        for _, row in attendance_df.iterrows():
            tree.insert("", "end", values=(row["Enrollment"], row["Name"]))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        close_btn = tk.Button(
            window,
            text="Close",
            command=window.destroy,
            bg="red",
            fg="white",
            font=("Arial", 12)
        )
        close_btn.pack(pady=10)
    
    def open_attendance_folder():
        sub = tx.get().strip()
        if sub == "":
            text_to_speech("Please enter the subject name")
            return
        
        folder_path = os.path.join(attendance_path, sub)
        if os.path.exists(folder_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(folder_path)
                elif os.name == 'posix':  # Linux/Mac
                    os.system(f'open "{folder_path}"' if sys.platform == "darwin" else f'xdg-open "{folder_path}"')
            except Exception as e:
                text_to_speech("Cannot open attendance folder")
        else:
            text_to_speech("No attendance records found for this subject")
    
    # Create main window
    subject_window = tk.Toplevel()
    subject_window.title("Attendance System - Subject Selection")
    subject_window.geometry("500x350")
    subject_window.configure(bg="#2C3E50")
    subject_window.resizable(False, False)
    
    # Title
    title_label = tk.Label(
        subject_window,
        text="Enter Subject Name",
        bg="#2C3E50",
        fg="#ECF0F1",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=20)
    
    # Subject entry frame
    entry_frame = tk.Frame(subject_window, bg="#2C3E50")
    entry_frame.pack(pady=20)
    
    subject_label = tk.Label(
        entry_frame,
        text="Subject:",
        bg="#2C3E50",
        fg="#ECF0F1",
        font=("Arial", 14)
    )
    subject_label.grid(row=0, column=0, padx=10, pady=10)
    
    tx = tk.Entry(
        entry_frame,
        width=20,
        font=("Arial", 14),
        bg="#34495E",
        fg="#ECF0F1",
        insertbackground="white"
    )
    tx.grid(row=0, column=1, padx=10, pady=10)
    
    # Buttons frame
    button_frame = tk.Frame(subject_window, bg="#2C3E50")
    button_frame.pack(pady=30)
    
    fill_btn = tk.Button(
        button_frame,
        text="Take Attendance",
        command=FillAttendance,
        bg="#27AE60",
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        height=2
    )
    fill_btn.grid(row=0, column=0, padx=10)
    
    view_btn = tk.Button(
        button_frame,
        text="View Records",
        command=open_attendance_folder,
        bg="#3498DB",
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        height=2
    )
    view_btn.grid(row=0, column=1, padx=10)
    
    # Notification label
    Notifica = tk.Label(
        subject_window,
        text="",
        bg="#2C3E50",
        fg="#F39C12",
        font=("Arial", 12),
        wraplength=400
    )
    Notifica.pack(pady=20)
    
    # Focus on entry field
    tx.focus_set()

# Test function
def test_face_recognition():
    """Test if face recognition is working"""
    print("Testing face recognition setup...")
    
    # Test OpenCV

    # print(f"OpenCV version: {cv2.__version__}")
    
    # Test face recognizer
    recognizer = create_face_recognizer()
    if recognizer:
        print("✓ Face recognition: WORKING")
        return True
    else:
        print("✗ Face recognition: NOT WORKING")
        print("Please install: pip install opencv-contrib-python")
        return False

if __name__ == "__main__":
    # Test the installation
    test_face_recognition()