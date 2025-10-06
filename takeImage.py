import os
import cv2
import numpy as np
from PIL import Image

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    try:
        if l1 == "" and l2 == "":
            message.configure(text="Please enter the details first!")
            err_screen()
            return False
        elif l1 == "":
            message.configure(text="Please enter enrollment number!")
            err_screen()
            return False
        elif l2 == "":
            message.configure(text="Please enter name!")
            err_screen()
            return False
        else:
            try:
                cam = cv2.VideoCapture(0)
                detector = cv2.CascadeClassifier(haarcasecade_path)
                enrollment = l1
                name = l2
                
                # Create directory for the student
                sampleNum = 0
                student_dir = os.path.join(trainimage_path, f"{enrollment}_{name}")
                if not os.path.exists(student_dir):
                    os.makedirs(student_dir)
                
                message.configure(text="Taking images... Look at camera!")
                text_to_speech("Taking images. Look at the camera and wait for 5 seconds.")
                
                while True:
                    ret, img = cam.read()
                    if not ret:
                        message.configure(text="Failed to access camera!")
                        return False
                    
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        sampleNum += 1
                        
                        # Save the captured face
                        cv2.imwrite(f"{student_dir}/{sampleNum}.jpg", gray[y:y + h, x:x + w])
                        cv2.imshow("Face", img)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    elif sampleNum > 30:  # Take 30 samples
                        break
                
                cam.release()
                cv2.destroyAllWindows()
                
                # Check if images were actually saved
                if sampleNum > 0 and os.path.exists(student_dir) and len(os.listdir(student_dir)) > 0:
                    message.configure(text=f"Images Saved for {name}")
                    text_to_speech("Images captured successfully!")
                    return True
                else:
                    message.configure(text="Failed to capture images!")
                    # Clean up empty directory
                    if os.path.exists(student_dir) and len(os.listdir(student_dir)) == 0:
                        os.rmdir(student_dir)
                    return False
                    
            except Exception as e:
                message.configure(text=f"Error: {str(e)}")
                print(f"Error in TakeImage: {e}")
                return False
                
    except Exception as e:
        message.configure(text="Something went wrong!")
        print(f"Error in TakeImage: {e}")
        return False





















