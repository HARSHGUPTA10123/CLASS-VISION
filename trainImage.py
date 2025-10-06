import os
import cv2
import numpy as np
from PIL import Image
import pandas as pd

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer.create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        def getImagesAndLabels(path):
            imagePaths = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.jpg') or file.endswith('.png'):
                        imagePaths.append(os.path.join(root, file))
            
            faceSamples = []
            ids = []
            
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                
                # Extract id from directory name (format: enrollment_name)
                dir_name = os.path.basename(os.path.dirname(imagePath))
                try:
                    id_str = dir_name.split('_')[0]  # Get enrollment part
                    id = int(id_str)
                except:
                    continue
                
                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)
            
            return faceSamples, ids
        
        message.configure(text="Training started... Please wait!")
        text_to_speech("Training started. Please wait.")
        
        faces, ids = getImagesAndLabels(trainimage_path)
        
        if len(faces) == 0:
            message.configure(text="No faces found to train!")
            text_to_speech("No faces found for training.")
            return False
        
        recognizer.train(faces, np.array(ids))
        
        # Save the model
        model_dir = os.path.dirname(trainimagelabel_path)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
        recognizer.save(trainimagelabel_path)
        
        message.configure(text=f"Model trained successfully with {len(faces)} images!")
        text_to_speech("Model trained successfully!")
        return True
        
    except Exception as e:
        message.configure(text=f"Training failed: {str(e)}")
        print(f"Error in TrainImage: {e}")
        return False

