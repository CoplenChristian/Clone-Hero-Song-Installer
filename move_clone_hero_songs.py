import os
import time
import ctypes
from datetime import datetime, timedelta

import patoolib
import rarfile
import py7zr

DOWNLOAD_DIR = "C:/Users/cople/Downloads"
TARGET_DIR = "G:/Games/clonehero-win64/clonehero-win64/songs"

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

def main():
    moved_files = extract_files()
    
    if moved_files:
        dialog_text = f'The following files have been moved: \n{", ".join(moved_files)}'
    else:
        dialog_text = 'No files were moved.'
        
    ctypes.windll.user32.MessageBoxW(0, dialog_text, "File Extraction Report", 1)


if __name__ == "__main__":
    main()