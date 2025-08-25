import os

def remove_specific_files(directory):
    # List all files in the given directory
    for filename in os.listdir(directory):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        # Check if the file is a .dxf or .jpg file and its name is not '1.dxf' or '1.jpg'
        if filename.endswith('.dxf') or filename.endswith('.jpg'):
            if filename not in ['1.dxf', '1.jpg','clean-org.jpg','clean.jpg']:
                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_path}")


remove_specific_files('/usr/src/app')