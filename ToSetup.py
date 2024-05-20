import os
import sys
import winreg as reg
import win32com.client
import csv
import ctypes
import stat
import zipfile

def CreateExcelFile():
    # Define the path for the folder and the file
    folder_path = r'C:\CopyTrade'
    file_path = os.path.join(folder_path, 'Childs.csv')


    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    set_folder_permissions(folder_path)

    # Define the header and some sample data for the CSV file
    header = ['ClientName', 'Multiply', 'ClientId', 'ClientAPI']
    data = [
        ['Master', 1, '12312345', 'neknvrdnjndfkml'],
        ['Child 1', 1, '12312345', 'neknvrdnjndfkml'],
    ]

    # Check if the file already exists
    file_exists = os.path.exists(file_path)

    # Open the file in append mode if it exists, else create a new file
    with open(file_path, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:  # Only write the header if creating a new file
            writer.writerow(header)
        writer.writerows(data)

    print(f'CSV file created/updated at: {file_path}')

def set_folder_permissions(folder_path):
    try:
        # Grant full control to everyone
        os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f'Permissions set for folder: {folder_path}')
    except Exception as e:
        print(f'Failed to set permissions for folder: {folder_path}. Error: {e}')
        sys.exit(1)

def add_to_startup(exe_path, exe_name):
    try:
        # Access registry and add the executable path to the Run key
        key = reg.HKEY_CURRENT_USER
        key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Open the key to modify it
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

        # Set the value for the executable to run on startup
        reg.SetValueEx(open_key, exe_name, 0, reg.REG_SZ, exe_path)
        reg.CloseKey(open_key)
        
        print(f"Successfully added {exe_name} to startup")
    except Exception as e:
        print(f"Failed to add {exe_name} to startup: {e}")


def create_shortcut(target, shortcut_path, description, icon=None):
    try:
        """
        Creates a shortcut.

        :param target: The path to the executable file.
        :param shortcut_path: The path where the shortcut will be created.
        :param description: The description of the shortcut.
        :param icon: The path to the icon file, optional.
        """
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.Description = description
        if icon:
            shortcut.IconLocation = icon
        shortcut.save()
    except:
        print("Create shortcut error")

def add_to_start_menu(exe_path, shortcut_name):
    try:
        """
        Adds a shortcut to the Start Menu.

        :param exe_path: The path to the executable file.
        :param shortcut_name: The name of the shortcut.
        """
        start_menu_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
        shortcut_path = os.path.join(start_menu_path, f"{shortcut_name}.lnk")
        create_shortcut(exe_path, shortcut_path, shortcut_name)
    except:
        print("Add to startup error")

def add_to_desktop(exe_path, shortcut_name):
    try:
        """
        Adds a shortcut to the Desktop.

        :param exe_path: The path to the executable file.
        :param shortcut_name: The name of the shortcut.
        """
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        shortcut_path = os.path.join(desktop_path, f"{shortcut_name}.lnk")
        create_shortcut(exe_path, shortcut_path, shortcut_name)
    except:
        print("Add to desktop error")


def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f'Extracted {zip_path} to {extract_to}')
    except Exception as e:
        print(f'Failed to unzip file: {zip_path}. Error: {e}')
        sys.exit(1)



if __name__ == "__main__":
    # Ensure the script is running with administrator privileges
    if not os.path.exists('C:\\Windows\\System32\\cmd.exe'):
        print("This script requires administrative privileges to run.")
        sys.exit(1)

    # Define the executable name and path
    exe_name = "main"
    #exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'main.exe')
    exe_path = r'C:\CopyTrade\main.exe'
    
    # Unzip a file to the CopyTrade directory
    zip_file_path = r'./CopyTrading.zip'  # Change this to the path of your zip file
    unzip_file(zip_file_path, r'C:\CopyTrade')

    #create database csv file
    CreateExcelFile()


    # Add the executable to startup
    add_to_startup(exe_path, exe_name)
    
    shortcut_name = "CopyTrading"  # Name for the shortcut

    # Add shortcut to the Start Menu
    add_to_start_menu(exe_path, shortcut_name)

    # Add shortcut to the Desktop
    add_to_desktop(exe_path, shortcut_name)

    print("Shortcuts created successfully.")
