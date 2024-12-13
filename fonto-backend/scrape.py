import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Selenium WebDriver using the Service class
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to scrape links and save them to a file
def scrape_links():
    # Open the file in write mode
    with open("extracted_links.txt", "w") as file:
        # Iterate through pages
        for page in range(1, 338):  # Adjust the range to scrape all pages
            url = f"https://www.dafont.com/new.php?page={page}"
            print(f"Scraping URL: {url}")
            driver.get(url)

            # Wait for the page to load
            time.sleep(3)

            # Find all download links
            links = driver.find_elements(By.CSS_SELECTOR, "a.dl")
            if links:
                for link in links:
                    href = link.get_attribute("href")
                    print(href)  # Print the download link in the terminal
                    file.write(href + "\n")  # Write the link to the file
            else:
                print(f"No download links found on page {page}.")
    
    print("Links have been saved to 'extracted_links.txt'.")

# Start scraping
scrape_links()

# Close the browser
driver.quit()


