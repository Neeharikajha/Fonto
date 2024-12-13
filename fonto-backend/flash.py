import os
import json
import asyncio
import aiofiles
import aiohttp
from PIL import Image
import google.generativeai as genai
from tqdm.asyncio import tqdm_asyncio

class FontDescriptionGenerator:
    def __init__(self, 
                 folder_path, 
                 output_text_path, 
                 api_key, 
                 max_workers=8, 
                 batch_size=100):
        """
        Initialize the Font Description Generator
        
        :param folder_path: Path to folder containing font images
        :param output_text_path: Path to output text file for descriptions
        :param api_key: Google Generative AI API key
        :param max_workers: Maximum number of concurrent workers
        :param batch_size: Number of images to process in each batch
        """
        self.folder_path = folder_path
        self.output_text_path = output_text_path
        self.max_workers = max_workers
        self.batch_size = batch_size
        
        # Configure Google AI
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_processed_files(self):
        """
        Read already processed files from the output text file
        
        :return: Set of processed file names
        """
        processed_files = set()
        if os.path.exists(self.output_text_path):
            with open(self.output_text_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        processed_files.add(data.get('name_of_font', '') + '.jpg')
                    except json.JSONDecodeError:
                        continue
        return processed_files

    def validate_image_files(self):
        """
        Validate and count image files in the folder
        
        :return: List of valid image files
        """
        image_files = [
            f for f in os.listdir(self.folder_path)
            if (f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")) and 
                os.path.isfile(os.path.join(self.folder_path, f)) and 
                os.path.getsize(os.path.join(self.folder_path, f)) > 0)
        ]
        
        print(f"Total valid image files: {len(image_files)}")
        print(f"First 10 files: {image_files[:10]}")
        
        # Check for duplicate filenames
        duplicate_files = len(image_files) - len(set(image_files))
        if duplicate_files:
            print(f"Warning: Found {duplicate_files} duplicate filenames")
        
        return image_files

    async def generate_font_description(self, image_path):
        """
        Generate font description for a single image
        
        :param image_path: Path to the image file
        :return: Generated description or None
        """
        try:
            img = Image.open(image_path)
            
            # Extract font name from filename
            font_name = os.path.splitext(os.path.basename(image_path))[0]

            # Prepare prompt
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

            # Generate content
            response = self.model.generate_content(
                [prompt, img],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=1024
                )
            )

            return response.text

        except Exception as e:
            print(f"Error generating description for {image_path}: {e}")
            return None

    async def process_single_image(self, img_file, semaphore, processed_files):
        """
        Process a single image file
        
        :param img_file: Image filename
        :param semaphore: Async semaphore to limit concurrent tasks
        :param processed_files: Set of already processed files
        :return: Processing result
        """
        # Skip if already processed
        if img_file in processed_files:
            print(f"Skipping already processed file: {img_file}")
            return None

        async with semaphore:
            img_path = os.path.join(self.folder_path, img_file)
            description = await self.generate_font_description(img_path)
            
            if description:
                async with aiofiles.open(self.output_text_path, 'a', encoding='utf-8') as f:
                    await f.write(description + "\n")
                return description
            return None

    async def process_images_async(self):
        """
        Asynchronously process images in batches
        """
        # Validate and get image files
        image_files = self.validate_image_files()
        
        # Get already processed files
        processed_files = self.get_processed_files()
        print(f"Already processed {len(processed_files)} files")

        # Create semaphore to limit concurrent tasks
        semaphore = asyncio.Semaphore(self.max_workers)

        # Process images in batches
        for i in range(0, len(image_files), self.batch_size):
            batch = image_files[i:i+self.batch_size]
            
            # Create tasks for the batch
            tasks = [
                self.process_single_image(img_file, semaphore, processed_files)
                for img_file in batch
            ]
            
            # Use tqdm for progress tracking
            await tqdm_asyncio.gather(*tasks, desc=f"Processing Batch {i//self.batch_size + 1}")
            
            # Optional: Add a small delay between batches to prevent overwhelming the API
            await asyncio.sleep(2)

    def run(self):
        """
        Main method to run the font description generator
        """
        try:
            # Run the async processing
            asyncio.run(self.process_images_async())
            print("Font description generation completed successfully!")
        except Exception as e:
            print(f"Error during processing: {e}")

# Usage Example
if __name__ == "__main__":
    # IMPORTANT: Replace with your actual API key
    API_KEY = "xyz"
    
    # Configuration
    FOLDER_PATH = "output_images"  # Path to folder with font images
    OUTPUT_TEXT_PATH = "font_descriptions.txt"  # Output file for descriptions
    
    # Initialize and run the generator
    generator = FontDescriptionGenerator(
        folder_path=FOLDER_PATH, 
        output_text_path=OUTPUT_TEXT_PATH, 
        api_key=API_KEY,
        max_workers=16,  # Adjust based on your system's capabilities
        batch_size=100   # Adjust batch size as needed
    )
    
    generator.run()