import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the base url for jarir website
base_url = "https://www.jarir.com/sa-en/laptops.html"

# Define the number of pages to scroll
pages_to_scroll = 1

# Create an empty list to store the scraped data
data = []

# Initialize the Selenium webdriver
driver = webdriver.Chrome()  # You need to have the Chrome driver installed and available in PATH.

# Scroll through the pages and scrape data
for page in range(1, pages_to_scroll + 1):
    url = f"{base_url}?p={page}"
    driver.get(url)
    time.sleep(3)  # Give the page time to load dynamically loaded content

    # Scroll to the bottom of the page to load more products
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the updated page source after scrolling
    page_source = driver.page_source

    # Parse the updated page source using BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all the product cards in the page
    products = soup.find_all("div", class_="product-tile")

    # Loop through each product card
    for product in products:
        name = product.find("p", class_="product-title__title").text.strip()
        price = product.find("span", class_="price_alignment").text.strip()

        # Create a dictionary with the product details
        item = {
            "name": name,
            "price": price,
        }

        # Append the dictionary to the data list
        data.append(item)

    # Print a message indicating the progress
    print(f"Scraped page {page} of {pages_to_scroll}")

# Close the webdriver
driver.quit()

# Print the number of items scraped
print(f"Scraped {len(data)} items")

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = "jarir_laptops_data.xlsx"
df.to_excel(output_file, index=False)

print(f"Data saved to {output_file}")
