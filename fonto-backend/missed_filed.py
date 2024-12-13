import os

# File and folder paths
processed_list_file = "done_till_now.txt"
output_images_folder = "output_images"
missing_files_file = "missing_files.txt"

def find_missing_files(processed_file, images_folder, output_file):
    try:
        # Read processed names and normalize by stripping spaces and converting to lowercase for comparison
        with open(processed_file, 'r', encoding='utf-8') as file:
            processed_names = set(line.strip().lower() for line in file)

        # Get all image file names (without extension), but keep the exact original names
        image_files = [
            image for image in os.listdir(images_folder)
            if os.path.isfile(os.path.join(images_folder, image))
        ]

        # Find files in the folder not in the processed list (case-insensitive comparison)
        missing_files = [image for image in image_files if os.path.splitext(image)[0].lower() not in processed_names]

        # Write missing files to output, with exact filenames
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for name in missing_files:
                outfile.write(name + "\n")

        print(f"Missing files saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
find_missing_files(processed_list_file, output_images_folder, missing_files_file)
