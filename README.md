# CLASS VISION - Smart Attendance System



A modern, AI-powered attendance management system that uses facial recognition technology to automate student attendance tracking with high accuracy and efficiency.


## ✨ Features

- **🤖 AI-Powered Face Recognition** - Advanced facial detection and identification
- **📸 Smart Registration** - Easy student enrollment with automated image capture
- **⚡ Real-time Attendance** - Instant attendance marking with live camera feed
- **📊 Automated Reporting** - Generate detailed attendance reports in CSV format
- **🎨 Modern Dark UI** - Eye-friendly interface with responsive design
- **🔒 Secure & Reliable** - Local data storage with no cloud dependencies

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Webcam
- Windows/Linux/macOS

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HARSHGUPTA10123/CLASS-VISION.git
   cd CLASS-VISION
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Required Folders**
   ```bash
   # Create necessary directories for the application
   mkdir TrainingImage
   mkdir TrainingImageLabel
   mkdir StudentDetails
   mkdir Attendance
   ```

4. **Run the application**
   ```bash
   python attendance.py
   ```

## 📋 How It Works

### 1. Student Registration
- Click **"Register"** button
- Enter Enrollment Number and Name
- System captures 30 facial images automatically and stores in `TrainingImage/` folder
- AI model trains on the captured data

### 2. Take Attendance
- Select **"Take Attendance"**
- Choose subject name
- System detects faces in real-time and marks attendance
- Records saved with timestamps in `Attendance/` folder

### 3. View Reports
- Click **"View Attendance"**
- Browse attendance records by subject from `Attendance/` folder
- Export data for further analysis

## 🗂️ Project Structure

```
CLASS-VISION/
├── attendance.py              # Main application file
├── automaticAttedance.py      # Automatic attendance module
├── takeImage.py              # Image capture module
├── trainImage.py             # Model training module
├── show_attendance.py        # Attendance viewing module
├── haarcascade_frontalface_default.xml  # Face detection model
├── requirements.txt          # Python dependencies
├── TrainingImage/            # Student face database (create this folder)
├── TrainingImageLabel/       # Trained model files (create this folder)
├── StudentDetails/           # Student information (create this folder)
├── Attendance/               # Attendance records (create this folder)
└── UI_Image/                 # Application icons and images
```

## 🛠️ Technical Details

### Technologies Used
- **Python** - Core programming language
- **OpenCV** - Computer vision and image processing
- **Tkinter** - GUI development
- **PIL** - Image handling
- **NumPy** - Numerical computations
- **Pandas** - Data management
- **Haar Cascades** - Face detection algorithm
- **LBPH** - Face recognition algorithm

### Face Recognition Pipeline
1. **Face Detection** - Haar Cascade classifier
2. **Image Preprocessing** - Grayscale conversion and normalization
3. **Feature Extraction** - Local Binary Patterns Histograms (LBPH)
4. **Model Training** - Supervised learning on captured images stored in `TrainingImage/`
5. **Real-time Recognition** - Live camera feed processing

## 📸 Screenshots
FOR SCREENSHOTS VISIT THIS LINK:-

https://drive.google.com/drive/folders/1Ra9DFry6_WJ33CBOjV0W4rTjpRR3QoeM?usp=sharing


```

Update these paths in the respective files if needed:
```python
# File paths configuration
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
studentdetail_path = "./StudentDetails/studentdetails.csv"
```

## 🐛 Troubleshooting

### Common Issues:

1. **"TrainingImage folder not found"**
   ```bash
   # Solution: Create the folder manually
   mkdir TrainingImage
   ```

2. **Camera access denied**
   - Ensure no other application is using the camera
   - Grant camera permissions to Python

3. **Dependencies installation failed**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```


## 👨‍💻 Developer

**Harsh Gupta**
- GitHub: [@HARSHGUPTA10123](https://github.com/HARSHGUPTA10123)
- Project: CLASS VISION Attendance System

## 🙏 Acknowledgments

- OpenCV community for excellent computer vision libraries
- Python community for comprehensive documentation



