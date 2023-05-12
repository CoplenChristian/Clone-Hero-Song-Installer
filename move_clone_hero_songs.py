import os
import shutil
import zipfile
import patoolib
import rarfile
from datetime import datetime, timedelta

# Set Download Directory
downloads_dir = ""

# Set to diretory where clone hero songs are saved
target_dir = ""

# Get the current date and the date from 24 hours ago
current_date = datetime.now()
past_date = current_date - timedelta(hours=24)

for file in os.listdir(downloads_dir):
    file_path = os.path.join(downloads_dir, file)

    # Check if the file is a zip or rar file and if it was created within the last 24 hours
    if (file.endswith(".zip") or file.endswith(".rar")) and datetime.fromtimestamp(os.path.getctime(file_path)) > past_date:
        
        # Open the zip or rar file
        if file.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                # Get the name of the folder to create in the target directory
                folder_name = os.path.splitext(file)[0].replace(" ", "-")

                # Extract the contents of the zip file to the target directory
                for obj in zip_ref.infolist():
                    if obj.filename.endswith('/'):
                        continue
                    else:
                        with zip_ref.open(obj) as file:
                            filename = os.path.basename(obj.filename)
                            target_file_path = os.path.join(target_dir, folder_name, filename.replace(" ", "-"))
                            target_file_dir = os.path.dirname(target_file_path)
                            if not os.path.exists(target_file_dir):
                                os.makedirs(target_file_dir)
                            with open(target_file_path, "wb") as target_file:
                                shutil.copyfileobj(file, target_file)

        elif file.endswith(".rar"):
            with rarfile.RarFile(file_path, "r") as rar_ref:
                # Get the name of the folder to create in the target directory
                folder_name = os.path.splitext(file)[0].replace(" ", "-")

                # Extract the contents of the rar file to the target directory
                for obj in rar_ref.infolist():
                    if obj.isdir():
                        continue
                    else:
                        filename = obj.filename.replace("\\", "/")
                        target_file_path = os.path.join(target_dir, folder_name, os.path.basename(filename).replace(" ", "-"))
                        target_file_dir = os.path.dirname(target_file_path)
                        if not os.path.exists(target_file_dir):
                            os.makedirs(target_file_dir)
                        with open(target_file_path, "wb") as target_file:
                            target_file.write(rar_ref.read(filename))

        # Delete the file from the downloads directory when done
        os.remove(file_path)