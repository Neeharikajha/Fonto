import os
import json

# File paths
processed_file = "continue_desc.txt"
missing_files_file = "missing_files.txt"
updated_missing_files_file = "updated_missing_files.txt"

def update_missing_files(processed_file, missing_files_file, updated_missing_files_file):
    try:
        # Read processed files from JSON
        processed_files = set()
        if os.path.exists(processed_file):
            with open(processed_file, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        data = json.loads(line.strip())
                        font_name = data.get('name_of_font', '').strip().lower()
                        if font_name:
                            processed_files.add(font_name)
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON line: {line.strip()}")
                        continue
        
        # Debug: Display processed files
        print(f"Processed files: {processed_files}")

        # Read missing files
        with open(missing_files_file, 'r', encoding='utf-8') as file:
            missing_files = [line.strip() for line in file]

        # Debug: Display missing files
        print(f"Missing files before filtering: {missing_files}")

        # Normalize and filter missing files
        updated_missing_files = [
            file for file in missing_files
            if os.path.splitext(file)[0].lower() not in processed_files
        ]

        # Debug: Display updated missing files
        print(f"Updated missing files: {updated_missing_files}")

        # Write updated missing files
        with open(updated_missing_files_file, 'w', encoding='utf-8') as outfile:
            for file_name in updated_missing_files:
                outfile.write(file_name + "\n")

        print(f"Updated missing files saved to: {updated_missing_files_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
update_missing_files(processed_file, missing_files_file, updated_missing_files_file)
