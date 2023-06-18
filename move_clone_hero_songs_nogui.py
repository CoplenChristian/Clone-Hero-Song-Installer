import os
import time
import json
from datetime import datetime, timedelta

import patoolib
import rarfile
import py7zr

CONFIG_FILE = "config.json"
DOWNLOAD_DIR = ""
TARGET_DIR = ""

def extract_files():
    moved_files = []
    one_day_ago = datetime.now() - timedelta(days=1)

    for filename in os.listdir(DOWNLOAD_DIR):
        file = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.isfile(file):
            last_modified_time = datetime.fromtimestamp(os.path.getmtime(file))
            if last_modified_time > one_day_ago:
                if filename.endswith('.zip'):
                    patoolib.extract_archive(file, outdir=TARGET_DIR)
                    moved_files.append(filename)
                elif filename.endswith('.rar'):
                    with rarfile.RarFile(file) as rf:
                        rf.extractall(TARGET_DIR)
                        moved_files.append(filename)
                elif filename.endswith('.7z'):
                    with py7zr.SevenZipFile(file, mode='r') as z:
                        z.extractall(TARGET_DIR)
                        moved_files.append(filename)
                
                os.remove(file)  # delete the archive file after extraction
                
    return moved_files

def save_config():
    config = {"DOWNLOAD_DIR": DOWNLOAD_DIR, "TARGET_DIR": TARGET_DIR}
    with open(CONFIG_FILE, "w") as outfile:
        json.dump(config, outfile)

def load_config():
    global DOWNLOAD_DIR
    global TARGET_DIR
    try:
        with open(CONFIG_FILE) as json_file:
            data = json.load(json_file)
            DOWNLOAD_DIR = data["DOWNLOAD_DIR"]
            TARGET_DIR = data["TARGET_DIR"]
    except Exception as e:
        print(f"Error loading config file: {e}")
        pass

def main():
    global DOWNLOAD_DIR
    global TARGET_DIR
    
    load_config()
    print(f"Current Download Directory: {DOWNLOAD_DIR}")
    print(f"Current Target Directory: {TARGET_DIR}")

    change_dir = input("Do you want to change the directories? (y/n): ")
    if change_dir.lower() == 'y':
        DOWNLOAD_DIR = input("Enter the new Download Directory: ")
        TARGET_DIR = input("Enter the new Target Directory: ")
        save_config()

    print("Running the file extraction...")
    moved_files = extract_files()
    
    if moved_files:
        print(f'The following files have been moved: \n{", ".join(moved_files)}')
    else:
        print('No files were moved.')

if __name__ == "__main__":
    main()