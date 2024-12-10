import os
import requests
from zipfile import ZipFile
import shutil
from PIL import Image, ImageDraw, ImageFont

# Directory to save downloaded files and extracted .otf and .ttf files
DOWNLOAD_DIR = "downloads"
EXTRACT_DIR = "extracted_fonts"
OUTPUT_DIR = "output_images"

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to download files from the first 5 links
def download_links(file_path):
    with open(file_path, "r") as f:
        links = f.readlines()  # Only take the first 'limit' links
    
    for index, link in enumerate(links):
        link = link.strip()
        if not link:
            continue
        
        try:
            print(f"Downloading {link} ({index + 1}/{len(links)})...")
            response = requests.get(link, stream=True)
            response.raise_for_status()

            # Determine filename
            filename = os.path.join(DOWNLOAD_DIR, f"font_{index + 1}.zip")
            with open(filename, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Failed to download {link}: {e}")

# Function to extract .otf and .ttf files from downloaded archives
def extract_font_files():
    for file in os.listdir(DOWNLOAD_DIR):
        file_path = os.path.join(DOWNLOAD_DIR, file)
        if file.endswith(".zip"):
            try:
                with ZipFile(file_path, "r") as zip_ref:
                    for zip_info in zip_ref.infolist():
                        # Check if file is either .otf or .ttf
                        if zip_info.filename.endswith(".otf") or zip_info.filename.endswith(".ttf"):
                            zip_info.filename = os.path.basename(zip_info.filename)  # Ensure a flat structure
                            zip_ref.extract(zip_info, EXTRACT_DIR)
                            print(f"Extracted: {zip_info.filename}")
            except Exception as e:
                print(f"Failed to extract {file}: {e}")

# Function to convert font files into images
def convert_fonts_to_images():
    text_to_render = "The quick brown fox jumps over the lazy dog !#$%*&"  # Text to render on images
    for font_file in os.listdir(EXTRACT_DIR):
        font_path = os.path.join(EXTRACT_DIR, font_file)
        
        if font_file.endswith(".otf") or font_file.endswith(".ttf"):
            try:
                # Load the font
                font = ImageFont.truetype(font_path, 60)  # You can adjust the size
                
                # Create a temporary image to calculate text size
                temp_img = Image.new('RGB', (1, 1), color='white')
                d = ImageDraw.Draw(temp_img)
                
                # Use textbbox() instead of textsize()
                bbox = d.textbbox((0, 0), text_to_render, font=font)
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                
                # Set the image size dynamically based on text width and height
                img_width = text_width + 40  # Adding some padding
                img_height = text_height + 40  # Adding some padding
                
                # Create an image with white background
                img = Image.new('RGB', (img_width, img_height), color='white')
                d = ImageDraw.Draw(img)
                
                # Position and text to render
                position = ((img_width - text_width) // 2, (img_height - text_height) // 2)
                
                # Render text on image
                d.text(position, text_to_render, font=font, fill='black')
                
                # Save the image as .jpg
                img_output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(font_file)[0]}.jpg")
                img.save(img_output_path)
                print(f"Image saved: {img_output_path}")
            except Exception as e:
                print(f"Failed to convert {font_file}: {e}")

# Step 1: Download the first 5 links from "extracted_files.txt"
download_links("extracted_links.txt")

# Step 2: Extract .otf and .ttf files
extract_font_files()

# Step 3: Convert extracted fonts to images
convert_fonts_to_images()

print(f"All images are saved in the '{OUTPUT_DIR}' directory.")
