import os
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.dsf import DSF
import tkinter as tk
from tkinter import filedialog

def rename_folder(folder_path, name_format):
  # Get a list of all the files in the directory
  file_list = os.listdir(folder_path)
  
  # Find the first audio file in the folder
  for file in file_list:
    if file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.wav') or file.endswith('.dsf'):
      audio_file = file
      break
  
  # Extract the metadata from the audio file
  audio = mutagen.File(os.path.join(folder_path, audio_file))
  
  # Extract the metadata tags depending on the file format
  if isinstance(audio, MP3):
    title = audio['TIT2'].text[0]
    artist = audio['TPE1'].text[0]
    album = audio['TALB'].text[0]
    genre = audio['TCON'].text[0]
    date = audio['TORY'].text[0]
  elif isinstance(audio, FLAC):
    title = audio['title'][0]
    artist = audio['artist'][0]
    album = audio['album'][0]
    genre = audio['genre'][0]
    date = audio['date'][0]
  elif isinstance(audio, WavPack):
    title = audio['title'][0]
    artist = audio['artist'][0]
    album = audio['album'][0]
    genre = audio['genre'][0]
    date = audio['date'][0]
  elif isinstance(audio, DSF):
    title = audio['title'][0]
    artist = audio['artist'][0]
    album = audio['album'][0]
    genre = audio['genre'][0]
    date = audio['date'][0]
    
  # Construct the new name for the folder using the specified format
  new_name = name_format.format(artist=artist, title=title, album=album, genre=genre, date=date)
  
  # Add a number in parentheses to the end of the name if it already exists
  counter = 0
  while os.path.exists(os.path.join(os.path.dirname(folder_path), new_name)):
    counter += 1
    new_name = name_format.format(artist=artist, title=title, album=album, genre=genre, date=date) + ' (' + str(counter) + ')'
  
  # Rename the folder
  os.rename(folder_path, os.path.join(os.path.dirname(folder_path), new_name))
  result_text.insert(tk.END, "Ancien nom : " + folder_path + " Nouveau nom : " + os.path.join(os.path.dirname(folder_path), new_name) + "\n")

# Create the main window
window = tk.Tk()

# Set the title of the window
window.title("TGN Tools")

# Make the window resizable
window.resizable(True, True)

# Create a list of pre-defined name formats
name_formats = [
    "{artist} - {album}",
    "{artist} - {title}",
    "{artist} - {album} ({date})",
    "{title}",
    "{title} - {artist}",
    "{album} ({date})",
    "{genre} - {artist} - {album}",
    "{genre} - {title} ({date})",
]
# Create a function to insert the selected name format into the name format field
def insert_name_format(event):
    selected_format = selected_name_format.get()
    name_format_field.delete(0, tk.END)
    name_format_field.insert(0, selected_format)

# Create a label for the name format field
name_format_label = tk.Label(window, text="Name format:")
name_format_label.grid(row=0, column=0, padx=5, pady=5)

# Create a variable to store the selected name format
selected_name_format = tk.StringVar()

# Set the default name format
selected_name_format.set(name_formats[0])

# Create a dropdown menu for the name formats
name_format_menu = tk.OptionMenu(window, selected_name_format, *name_formats, command=insert_name_format)
name_format_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Create a label for the file browser button
file_browser_label = tk.Label(window, text="Select directories to rename:")
file_browser_label.grid(row=1, column=0, padx=5, pady=5)

# Create a text field for the user to enter the folder name format
name_format_field = tk.Entry(window)
name_format_field.grid(row=1, column=1, padx=5, pady=5)

# Bind the <<MenuSelect>> event to the insert_name_format function
name_format_menu.bind("<<MenuSelect>>", insert_name_format)

# Create a function to open the file browser and get the selected directories
def select_directories():
    result_text.delete(tk.END)
    directories = filedialog.askdirectory(parent=window, title='Select directories to rename')
    if directories:
        # Split the directories into a list of individual directories
        directories = directories.split(';')
        
        # Get the folder name format entered by the user
        name_format = name_format_field.get()
        
        # Rename each directory
        for directory in directories:
            rename_folder(directory, name_format)

# Create a button to open the file browser
button = tk.Button(text='Select directories', command=select_directories)
button.grid(row=2, column=0, padx=5, pady=5)

# create a text area to show the results of renaming
result_text = tk.Text(window)
result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# add a button to clear the text area 
clear_button = tk.Button(text='Clear results', command=lambda: result_text.delete(1.0, tk.END))
clear_button.grid(row=4, column=0, padx=5, pady=5)

# Run the main loop
window.mainloop()
