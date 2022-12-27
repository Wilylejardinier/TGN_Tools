import os
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.dsf import DSF
import tkinter as tk
from tkinter import filedialog

def rename_folder(folder_path):
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
  elif isinstance(audio, FLAC):
    title = audio['title'][0]
    artist = audio['artist'][0]
  elif isinstance(audio, WavPack):
    title = audio['title'][0]
    artist = audio['artist'][0]
  elif isinstance(audio, DSF):
    title = audio['title'][0]
    artist = audio['artist'][0]
  
  # Construct the new name for the folder
  new_name = artist + ' - ' + title
  
  # Rename the folder
  os.rename(folder_path, os.path.join(os.path.dirname(folder_path), new_name))

# Create the main window
window = tk.Tk()

# Make the window movable
window.resizable(True, True)

# Create a function to open the file browser and get the selected directories
def select_directories():
  directories = filedialog.askdirectory(parent=window, title='Select directories to rename')
  if directories:
    # Split the directories into a list of individual directories
    directories = directories.split(';')
    
    # Rename each directory
    for directory in directories:
      rename_folder(directory)

# Create a button to open the file browser
button = tk.Button(text='Select directories', command=select_directories)
button.pack()

# Run the main loop
window.mainloop()
