import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import sys

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        # Check if attendance folder exists for this subject
        subject_folder = os.path.join("Attendance", Subject)
        if not os.path.exists(subject_folder):
            t = f"No attendance records found for {Subject}"
            text_to_speech(t)
            print(f"✗ Folder not found: {subject_folder}")
            return
        
        # Find all CSV files for this subject
        pattern = os.path.join("Attendance", Subject, f"{Subject}_*.csv")
        filenames = glob(pattern)
        
        if not filenames:
            t = f"No attendance files found for {Subject}"
            text_to_speech(t)
            print(f"✗ No files found matching: {pattern}")
            return
        
        print(f"✓ Found {len(filenames)} attendance files for {Subject}")
        
        try:
            # Read all CSV files
            df = [pd.read_csv(f) for f in filenames]
            if not df:
                t = "No valid attendance data found"
                text_to_speech(t)
                return
            
            # Merge all dataframes
            newdf = df[0]
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            
            newdf.fillna(0, inplace=True)
            
            # Calculate attendance percentage
            if len(newdf.columns) > 2:  # Check if we have date columns
                newdf["Attendance"] = 0
                for i in range(len(newdf)):
                    date_columns = newdf.iloc[i, 2:-1]  # Get all date columns
                    if len(date_columns) > 0:
                        attendance_percentage = int(round(date_columns.mean() * 100))
                        newdf["Attendance"].iloc[i] = f"{attendance_percentage}%"
            
            # Save merged attendance
            output_path = os.path.join("Attendance", Subject, "attendance.csv")
            newdf.to_csv(output_path, index=False)
            
            # Display attendance in window
            display_attendance_table(newdf, Subject)
            
        except Exception as e:
            error_msg = f"Error processing attendance: {str(e)}"
            print(f"✗ {error_msg}")
            text_to_speech("Error processing attendance data")
    
    def display_attendance_table(df, subject):
        """Display attendance in a new window"""
        root = tk.Toplevel()
        root.title(f"Attendance of {subject}")
        root.configure(background="black")
        root.geometry("800x400")
        
        # Create a frame for the table
        frame = tk.Frame(root, bg="black")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a text widget to display the data
        text_widget = tk.Text(
            frame,
            width=100,
            height=20,
            bg="black",
            fg="yellow",
            font=("Courier New", 12),
            relief=tk.RIDGE
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
        
        # Convert dataframe to string and display
        df_string = df.to_string(index=False)
        text_widget.insert(tk.END, df_string)
        text_widget.config(state=tk.DISABLED)  # Make it read-only
        
        print(f"✓ Displaying attendance for {subject}")
        print(df)
    
    def Attf():
        """Open attendance folder"""
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            folder_path = os.path.join("Attendance", sub)
            if os.path.exists(folder_path):
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(folder_path)
                    elif os.name == 'posix':  # Linux/Mac
                        if sys.platform == "darwin":
                            os.system(f'open "{folder_path}"')
                        else:
                            os.system(f'xdg-open "{folder_path}"')
                    t = f"Opening attendance folder for {sub}"
                    text_to_speech(t)
                except Exception as e:
                    t = "Cannot open attendance folder"
                    text_to_speech(t)
                    print(f"Error opening folder: {e}")
            else:
                t = f"No attendance folder found for {sub}"
                text_to_speech(t)

    # Create subject selection window
    subject = tk.Tk()
    subject.title("View Attendance")
    subject.geometry("580x320")
    subject.resizable(False, False)
    subject.configure(background="black")

    # Title
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.pack(pady=20)

    # Subject entry frame
    entry_frame = tk.Frame(subject, bg="black")
    entry_frame.pack(pady=20)

    sub_label = tk.Label(
        entry_frame,
        text="Enter Subject:",
        width=12,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub_label.grid(row=0, column=0, padx=10)

    tx = tk.Entry(
        entry_frame,
        width=15,
        cursor="xterm",
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 20, "bold"),
        insertbackground="red",  # Red cursor for high visibility
        insertwidth=3,  # Thicker cursor
    )
    tx.grid(row=0, column=1, padx=10)
    tx.icursor(0)  # Set cursor at the beginning

    # Buttons frame
    button_frame = tk.Frame(subject, bg="black")
    button_frame.pack(pady=30)

    fill_a = tk.Button(
        button_frame,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=15,
        relief=RIDGE,
    )
    fill_a.grid(row=0, column=0, padx=20)

    attf = tk.Button(
        button_frame,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    attf.grid(row=0, column=1, padx=20)

    # Focus on entry field
    tx.focus_set()
    
    subject.mainloop()

# Test function
if __name__ == "__main__":
    def test_tts(text):
        print(f"TTS: {text}")
    
    subjectchoose(test_tts)