from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import random

# Configure WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service('C:/chromedriver.exe')  # Path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_product_data(sku):
    try:
        # Open Home Depot's website
        driver.get("https://www.homedepot.com/")
        print("Opened Home Depot website.")
        time.sleep(random.uniform(3, 5))  # Added random delay to mimic human behavior

        # Wait for the search bar to be present
        search_bar = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "typeahead-search-field-input"))
        )
        print("Search bar located.")
        time.sleep(random.uniform(2, 4))  # Added random delay to ensure the search bar is ready

        # Enter the SKU in the search bar and submit
        search_bar.clear()
        search_bar.send_keys(sku)
        search_bar.send_keys(Keys.RETURN)
        print(f"Searched for SKU: {sku}")
        time.sleep(random.uniform(5, 7))  # Added random delay to allow the page to start loading

        # Retry mechanism to handle page load and disappearing elements
        retries = 3
        while retries > 0:
            try:
                # Wait for the loading indicator to disappear
                WebDriverWait(driver, 60).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-indicator"))
                )
                print("Loading indicator disappeared.")
                
                # Wait for the product page to load
                product_page_loaded = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-title__title"))
                )
                if not product_page_loaded.is_displayed():
                    raise Exception("Product page is not visible.")
                print("Product page loaded.")
                time.sleep(random.uniform(3, 5))  # Added random delay to ensure the page is fully loaded

                # Scrape relevant product details
                product_details = {}
                product_details['title'] = driver.find_element(By.CSS_SELECTOR, "h1.product-title__title").text
                product_details['price'] = driver.find_element(By.CSS_SELECTOR, "div.price-format__main-price").text
                product_details['model_number'] = driver.find_element(By.CSS_SELECTOR, "div.product-meta__model").text
                product_details['sku_number'] = driver.find_element(By.CSS_SELECTOR, "div.product-meta__sku").text
                product_details['description'] = driver.find_element(By.CSS_SELECTOR, "div.product-description__content").text

                # Print the scraped data
                print("Scraped Product Data:")
                for key, value in product_details.items():
                    print(f"{key.capitalize()}: {value}")

                # Save the data to a JSON file
                with open(f"product_{sku}.json", "w") as json_file:
                    json.dump(product_details, json_file, indent=4)
                print(f"Product data saved to product_{sku}.json")

                return product_details

            except Exception as e:
                print(f"An error occurred while scraping (attempts left: {retries}): {e}")
                retries -= 1
                time.sleep(30)  # Wait for 30 seconds before retrying

        print("Failed to scrape the product data after multiple attempts.")

    finally:
        # Ensure the driver is closed after completion
        driver.quit()
        print("WebDriver closed.")

# Example usage
if __name__ == "__main__":
    sku = "1010845124"  # Replace with the actual SKU number
    scrape_product_data(sku)
