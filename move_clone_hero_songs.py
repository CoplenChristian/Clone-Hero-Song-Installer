import os
import time
import ctypes
from datetime import datetime, timedelta
import json
import tkinter as tk
from tkinter import filedialog

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
        pass

def select_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def main():
    load_config()
    root = tk.Tk()
    root.title("File Extractor")

    download_dir_entry = tk.Entry(root, width=50)
    download_dir_entry.insert(0, DOWNLOAD_DIR)
    download_dir_entry.grid(row=0, column=1, padx=20, pady=(10, 0))

    target_dir_entry = tk.Entry(root, width=50)
    target_dir_entry.insert(0, TARGET_DIR)
    target_dir_entry.grid(row=1, column=1)

    download_dir_button = tk.Button(root, text="Download Directory", command=lambda: select_directory(download_dir_entry))
    download_dir_button.grid(row=0, column=0, padx=20, pady=(10, 0))

    target_dir_button = tk.Button(root, text="Target Directory", command=lambda: select_directory(target_dir_entry))
    target_dir_button.grid(row=1, column=0)

    run_button = tk.Button(root, text="Run", command=lambda: run_task(download_dir_entry.get(), target_dir_entry.get()))
    run_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

def run_task(download_dir, target_dir):
    global DOWNLOAD_DIR
    global TARGET_DIR
    DOWNLOAD_DIR = download_dir
    TARGET_DIR = target_dir
    save_config()

    moved_files = extract_files()
    
    if moved_files:
        dialog_text = f'The following files have been moved: \n{", ".join(moved_files)}'
    else:
        dialog_text = 'No files were moved.'
        
    ctypes.windll.user32.MessageBoxW(0, dialog_text, "File Extraction Report", 1)


if __name__ == "__main__":
    main()