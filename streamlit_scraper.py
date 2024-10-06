import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

# Function to scrape data from the provided URL
def scrape_data(url):
    # Initialize the Chrome WebDriver using WebDriver Manager
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the webpage
    driver.get(url)
    
    # Wait for the page to load completely (adjust the sleep time if needed)
    time.sleep(5)

    # Get the page source and parse it using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Close the browser after page load
    driver.quit()

    # Find all product containers
    products = soup.find_all('div', class_='info')

    # Create a list to hold the scraped data
    scraped_data = []

    # Iterate through each product and extract details
    for product in products:
        # Extract product name
        name = product.find('h3', class_='name').text.strip()
        
        # Extract current price
        current_price = product.find('div', class_='prc').text.strip()
        
        # Extract old price (if available)
        old_price = product.find('div', class_='old')
        old_price = old_price.text.strip() if old_price else "N/A"
        
        # Extract discount (if available)
        discount = product.find('div', class_='bdg _dsct _sm')
        discount = discount.text.strip() if discount else "No Discount"
        
        # Extract ratings (if available)
        ratings = product.find('div', class_='stars _s')
        ratings = ratings.text.strip() if ratings else "No Ratings"

        # Append the product details to the list
        scraped_data.append([name, current_price, old_price, discount, ratings])

    return scraped_data

# Streamlit UI
st.title("Web Scraper")

# Input field for the URL
url = st.text_input("Enter the URL to scrape data from:")

if st.button("Scrape"):
    if url:
        try:
            # Call the scrape_data function
            data = scrape_data(url)

            # Create a DataFrame from the scraped data
            df = pd.DataFrame(data, columns=['Product Name', 'Current Price', 'Old Price', 'Discount', 'Ratings'])

            # Display the scraped data
            st.write("### Scraped Data:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
