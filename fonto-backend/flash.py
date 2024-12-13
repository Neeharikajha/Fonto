import os
from PIL import Image
import google.generativeai as genai
from tqdm import tqdm
import concurrent.futures
import json

def get_processed_files(output_text_path):
    """
    Read already processed files from the output text file
    """
    processed_files = set()
    if os.path.exists(output_text_path):
        with open(output_text_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    # Try to parse the JSON to extract the filename
                    data = json.loads(line.strip())
                    processed_files.add(data.get('name_of_font', '') + '.jpg')
                except json.JSONDecodeError:
                    continue
    return processed_files

def generate_font_description(image_path):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        img = Image.open(image_path)

        # Configure generative AI with the API key
        genai.configure(api_key="AIzaSyDdmhfcmDMRElLhTnDpg_ulf0jbvS5K1wA")

        # Use the model to generate the content description
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Extract font name from the image filename (without extension)
        font_name = os.path.splitext(os.path.basename(image_path))[0]

        # Generate content based on the image
        prompt = (
            f"Generate a detailed description of the font used in the image. "
            f"Provide the following details in JSON format, using '{font_name}' as the name of the font: "
            f"{{ "
            f"'name_of_font': '{font_name}', "
            f"'detailed_description': '<Detailed description of the font style>', "
            f"'personality': '<Personality of the font (e.g., elegant, bold, playful)>', "
            f"'practical_use': '<Practical uses for this font (e.g., advertising, logos)>', "
            f"'cultural_intuition': '<Cultural context or intuition of this font (e.g., widely used in western design)>', "
            f"'search_keywords': '<Relevant search keywords (e.g., sans-serif, modern, serif, minimal)>' "
            f"}} "
        )

        # Removed stream=True and adjusted generation config
        response = model.generate_content(
            [prompt, img],
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=1024  # Limit output size to reduce processing time
            )
        )

        return response.text

    except Exception as e:
        print(f"Error generating description for {image_path}: {e}")
        return None

def save_text_to_file(output_text_path, content):
    try:
        with open(output_text_path, 'a', encoding='utf-8') as text_file:
            text_file.write(content + "\n")
        print(f"Text file successfully updated: {output_text_path}")
    except Exception as e:
        print(f"Error saving text file: {e}")

def process_image(img_file, folder_path, output_text_path, processed_files):
    # Skip if already processed
    if img_file in processed_files:
        print(f"Skipping already processed file: {img_file}")
        return

    img_path = os.path.join(folder_path, img_file)
    description = generate_font_description(img_path)
    if description:
        save_text_to_file(output_text_path, description)

def process_images_in_folder(folder_path, output_text_path, max_workers=4):
    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        # Get already processed files
        processed_files = get_processed_files(output_text_path)
        print(f"Already processed {len(processed_files)} files")

        # List files in the folder
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))
        ]

        print(f"Total image files to process: {len(image_files)}")

        if len(image_files) == 0:
            print("No images found in the folder.")
            return

        # Use ThreadPoolExecutor for concurrent processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a list of futures
            futures = [
                executor.submit(process_image, img_file, folder_path, output_text_path, processed_files)
                for img_file in image_files
            ]

            # Use tqdm to show progress
            list(tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing images"))

    except Exception as e:
        print(f"Error processing folder: {e}")

# Usage Example
folder_path = "output_images"  # Path to the folder containing images
output_text_path = "the_descriptions.txt"  # Path to save the text file

# Process the images and generate descriptions
process_images_in_folder(folder_path, output_text_path)