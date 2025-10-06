import os
import shutil
import pandas as pd

def reset_everything():
    print("=== COMPLETELY DELETING EVERYTHING ===")
    print("This will remove ALL data and start fresh...")
    
    # List of everything to delete
    items_to_delete = [
        "TrainingImage",      # All training images
        "TrainingImageLabel", # Trained model
        "Attendance",         # Attendance records
        "StudentDetails",     # Student database
    ]
    
    # Delete everything
    for item in items_to_delete:
        if os.path.exists(item):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    print(f"✓ Deleted file: {item}")
                else:
                    shutil.rmtree(item)  # Remove folder and all contents
                    print(f"✓ Deleted folder: {item}")
            except Exception as e:
                print(f"✗ Error deleting {item}: {e}")
        else:
            print(f"ℹ {item} not found (already deleted)")
    
    # Recreate empty directories with proper structure
    directories_to_create = [
        "TrainingImage",           # For face images
        "TrainingImageLabel",      # For trained model
        "Attendance",              # For attendance records
        "StudentDetails",          # For student database
    ]
    
    for directory in directories_to_create:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created folder: {directory}")
    
    # Create empty student details CSV with proper headers
    empty_df = pd.DataFrame(columns=["Enrollment", "Name"])
    empty_df.to_csv("StudentDetails/studentdetails.csv", index=False)
    print("✓ Created empty student details CSV")
    
    print("\n" + "="*50)
    print("✅ COMPLETELY RESET SUCCESSFUL!")
    print("="*50)
    print("\nNow you can start fresh:")
    print("1. Register new students")
    print("2. Train the model") 
    print("3. Take attendance")
    print("\nAll previous data including ID 100 has been deleted!")

# Run the reset
if __name__ == "__main__":
    print("WARNING: This will delete ALL training data and start from scratch!")
    confirm = input("Are you absolutely sure? (type 'YES' to confirm): ")
    
    if confirm.upper() == 'YES':
        reset_everything()
        
        # Verification
        print("\n" + "="*50)
        print("VERIFICATION:")
        print("="*50)
        
        # Check if everything is clean
        check_items = ["TrainingImage", "TrainingImageLabel/Trainner.yml", "StudentDetails/studentdetails.csv"]
        
        all_clean = True
        for item in check_items:
            if os.path.exists(item):
                if os.path.isdir(item):
                    item_count = len(os.listdir(item))
                else:
                    # For CSV, check if empty (only headers)
                    try:
                        df = pd.read_csv(item)
                        item_count = len(df)
                    except:
                        item_count = 1
                
                if item_count == 0:
                    print(f"✓ {item}: Clean")
                else:
                    print(f"⚠ {item}: Not empty ({item_count} items)")
                    all_clean = False
            else:
                print(f"✓ {item}: Deleted")
        
        if all_clean:
            print("\n🎉 SYSTEM IS COMPLETELY CLEAN AND READY!")
        else:
            print("\n⚠ Some items still contain data. Manual cleanup may be needed.")
            
    else:
        print("Reset cancelled. No changes were made.")