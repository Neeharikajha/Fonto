# import json
# import re

# # Input and output file paths
# input_file = ["the_descriptions.txt", "continue_desc.txt"]
# output_file = "done_till_now.txt"

# def extract_and_save_font_names(input_path, output_path):
#     try:
#         font_names = []

#         # Read the entire file content
#         with open(input_path, 'r', encoding='utf-8') as infile:
#             content = infile.read()

#             # Use regex to extract JSON objects (assuming they are wrapped in braces)
#             json_blocks = re.findall(r'{.*?}', content, re.DOTALL)

#             for block in json_blocks:
#                 try:
#                     # Parse each JSON block
#                     font_data = json.loads(block)
#                     font_name = font_data.get("name_of_font")
#                     if font_name:
#                         font_names.append(font_name)
#                 except json.JSONDecodeError as e:
#                     print(f"Skipping invalid JSON block due to error: {e}\nBlock: {block}")

#         # Write font names to the output file
#         with open(output_path, 'w', encoding='utf-8') as outfile:
#             for name in font_names:
#                 outfile.write(name + "\n")

#         print(f"Font names have been saved to: {output_path}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Run the function
# extract_and_save_font_names(input_file, output_file)

import json
import re

# Input and output file paths
input_files = ["the_descriptions.txt", "continue_desc.txt"]
output_file = "done_till_now.txt"

def extract_and_save_font_names(input_paths, output_path):
    try:
        font_names = []

        # Process each file in the input list
        for input_path in input_paths:
            try:
                # Read the entire file content
                with open(input_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()

                    # Use regex to extract JSON objects (assuming they are wrapped in braces)
                    json_blocks = re.findall(r'{.*?}', content, re.DOTALL)

                    for block in json_blocks:
                        try:
                            # Parse each JSON block
                            font_data = json.loads(block)
                            font_name = font_data.get("name_of_font")
                            if font_name:
                                font_names.append(font_name)
                        except json.JSONDecodeError as e:
                            print(f"Skipping invalid JSON block in {input_path} due to error: {e}\nBlock: {block}")

            except FileNotFoundError:
                print(f"File not found: {input_path}")

        # Write all extracted font names to the output file
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for name in font_names:
                outfile.write(name + "\n")

        print(f"Font names from all files have been saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
extract_and_save_font_names(input_files, output_file)
