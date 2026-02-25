import os
import shutil

# Files to delete
files_to_delete = [
    'CHARACTER_IMAGES.md',
    'cleanup.py',
    'DEPLOYMENT.md',
    'habit_data.csv',
    'images_README.md',
    'survey_data.csv',
    'UPLOAD_CHECKLIST.md',
    'UPLOAD_MEME_FOLDER.md'
]

# Folders to delete
folders_to_delete = ['male', 'meme']

# Delete files
for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)
        print(f"Deleted: {file}")

# Delete folders
for folder in folders_to_delete:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Deleted folder: {folder}")

# Rename thank.webp to thank.jpg
if os.path.exists('thank.webp'):
    os.rename('thank.webp', 'thank.jpg')
    print("Renamed: thank.webp -> thank.jpg")

print("\nCleanup complete! ✅")
