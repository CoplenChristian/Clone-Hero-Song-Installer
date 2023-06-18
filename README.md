# Clone-Hero-Song-Installer

The Song Installer program comes in two versions: a graphical user interface (GUI) version and a command-line interface (CLI) version. Both versions handle the extraction of various archive files (.zip, .rar, and .7z) from a specified downloads directory and move the extracted contents to a target directory. The directories are configurable and the settings are saved between sessions.
Prerequisites

## These scripts require Python and the following Python packages:

    patoolib for handling .zip files
    rarfile for handling .rar files
    py7zr for handling .7z files

You can install these with pip:

pip install patoolib rarfile py7zr

## GUI Version (move_clone_hero_songs.py)

The GUI version presents a simple window with two fields for the downloads and target directories. Clicking the associated buttons will open a directory selection dialog. The selected directories can also be manually edited in the fields.

Clicking the "Run" button will start the extraction process. Once complete, a dialog box will display a list of moved files or a message saying that no files were moved.

The directories are saved in a configuration file (config.json) every time the "Run" button is clicked and are loaded from this file every time the program starts.

To run the GUI version, navigate to the directory containing the script in a terminal and enter:

python extract_gui.py

## CLI Version (move_clone_hero_songs_nogui.py)

The CLI version is run in a terminal and presents text output. On start, it will display the current downloads and target directories and ask if you want to change them. If yes, it will prompt for the new directories and save them to a configuration file (config.json).

It will then start the extraction process and print a list of moved files or a message saying that no files were moved.

To run the CLI version, navigate to the directory containing the script in a terminal and enter:

python extract_cli.py

Note

The directories in the configuration file are stored as absolute paths, so moving the directories on the filesystem after they have been set may cause errors. If you encounter errors, try resetting the directories.
