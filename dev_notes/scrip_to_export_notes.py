import subprocess

# Set the path to the Notes app
app_path = "Notes"

# Set the path to the folder where the exported notes will be saved
export_folder = "/Users/ljw303/Documents/Notes"

# Get the IDs of all notes in the Notes app
applescript = f'tell application "{app_path}" to get id of every note'
note_ids = subprocess.check_output(['osascript', '-e', applescript]).decode('utf-8').split(', ')

# Loop through each note ID and export the note as a text file
for note_id in note_ids:
    # Get the title and body of the note
    applescript = f'tell application "{app_path}" to get name of note id "{note_id}"'
    note_title = subprocess.check_output(['osascript', '-e', applescript]).strip().decode('utf-8')
    applescript = f'tell application "{app_path}" to get body of note id "{note_id}"'
    note_body = subprocess.check_output(['osascript', '-e', applescript]).strip().decode('utf-8')
    
    # Write the note to a text file in the export folder
    filename = f"{note_title}.txt"
    filepath = f"{export_folder}/{filename}"
    with open(filepath, "w") as file:
        file.write(note_body)