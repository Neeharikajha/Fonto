import json
import re

def convert_to_json(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            # Read the entire file content
            file_content = infile.read()
            
            # Find all JSON blocks using regex
            json_matches = re.findall(r'```json\n(.*?)\n```', file_content, re.DOTALL)
            
            # Parse each JSON block
            data_list = []
            for json_str in json_matches:
                try:
                    # Parse the JSON string
                    json_data = json.loads(json_str.strip())
                    data_list.append(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
            
            # Write to output file
            if data_list:
                with open(output_filename, 'w') as outfile:
                    json.dump(data_list, outfile, indent=4)
                print(f"Successfully converted {len(data_list)} JSON objects")
            else:
                print("No valid JSON objects found")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
input_filename = 'continue_desc.txt'
output_filename = 'the_descriptions_pt2.json'
convert_to_json(input_filename, output_filename)