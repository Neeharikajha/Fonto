import os

# Specify the folder path
output_images_folder = "output_images"

# Count the number of files in the folder
def count_files(folder_path):
    try:
        # List all files and filter out directories
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        print(f"Number of files in '{folder_path}': {len(files)}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
count_files(output_images_folder)
