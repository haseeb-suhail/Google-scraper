import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import re
from selenium.common.exceptions import NoSuchElementException

# Initialize the ChromeDriver with options and services
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    '--user-agent=%s' % "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('profile-directory=default')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.google.com/maps')
driver.maximize_window()
sleep(3)


# Function to extract social media links (not currently used but kept for reference)
def social_media_links():
    try:
        page_source = driver.page_source
        social_media_links = []

        if "linkedin.com" in page_source:
            linkedin_link = driver.find_element(By.XPATH, "//a[contains(@href, 'linkedin.com')]")
            social_media_links.append(linkedin_link.get_attribute("href"))

        if "twitter.com" in page_source:
            twitter_link = driver.find_element(By.XPATH, "//a[contains(@href, 'twitter.com')]")
            social_media_links.append(twitter_link.get_attribute("href"))

        if "instagram.com" in page_source:
            instagram_link = driver.find_element(By.XPATH, "//a[contains(@href, 'instagram.com')]")
            social_media_links.append(instagram_link.get_attribute("href"))

        if "facebook.com" in page_source:
            facebook_link = driver.find_element(By.XPATH, "//a[contains(@href, 'facebook.com')]")
            social_media_links.append(facebook_link.get_attribute("href"))

        if social_media_links:
            print("Social Media Links:", ", ".join(social_media_links))
        else:
            print("No social media links found")
        sleep(4)
    except:
        pass


# Main loop for processing multiple states
while True:
    state = input('Enter input (or type "exit" to quit)G: ')
    if state.lower() == 'exit':
        break

    search_bar = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    search_bar.clear()
    search_bar.send_keys(f'{state}')
    search_bar.send_keys(Keys.RETURN)
    sleep(5)

    panel_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]'
    sleep(4)
    scrollable_div = driver.find_element(By.XPATH, panel_xpath)

    # Initialize CSV writer with appropriate headers
    output_csv = open(f'Exotic Snacks in {state}.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(output_csv)
    headers = ['Company Name', 'Full Address', 'Category', 'Phone No', 'Company Website',
               'Google Map Url']
    writer.writerow(headers)

    # Scroll and gather results
    results_found = set()
    flag = True
    while flag:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        sleep(2)
        results = driver.find_elements(By.CLASS_NAME, 'Nv2PK')
        print('Results:', len(results))
        for result in results:
            if result not in results_found:
                results_found.add(result)
        if len(results_found) == len(results):
            flag = False

    # Loop to extract all data
    index = 1
    for result in results_found:
        try:
            # Initializing all variables with none value in it
            Company_Name = Full_address = Category = Phone_number = Company_website = latitude = longitude = Google_map_link = None

            result.click()
            sleep(2)
            try:
                Company_Name = driver.find_element(By.XPATH,
                                                   '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1').text.strip()
                sleep(1)
            except NoSuchElementException:
                Company_Name = "Not found"

            try:
                Category = driver.find_element(By.XPATH,
                                               '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button').text.strip()
            except NoSuchElementException:
                Category = "Not found"

            try:
                address = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label^="Address"]')
                for button in address:
                    Full_address = button.get_attribute('aria-label').replace("Address: ", "")
                    Full_address = Full_address.strip()
                    sleep(1)
            except NoSuchElementException:
                Full_address = "Not found"

            try:
                phone_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Phone:")]')
                phone_label = phone_button.get_attribute('aria-label')
                phone_regex = r"Phone: ([^']+)"
                match = re.search(phone_regex, phone_label)
                if match:
                    Phone_number = match.group(1)
            except NoSuchElementException:
                Phone_number = "Not found"

            try:
                website_link = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Website:")]')
                aria_label = website_link.get_attribute("aria-label")
                website_regex = r"Website: (.+)"
                match = re.search(website_regex, aria_label)
                if match:
                    Company_website = match.group(1)
            except NoSuchElementException:
                Company_website = "Not found"

            try:
                Google_map_link = driver.current_url
                match = re.search(r'@([\d.-]+),([\d.-]+)', Google_map_link)
                if match:
                    latitude = match.group(1)
                    longitude = match.group(2)
            except NoSuchElementException:
                latitude = longitude = "Not found"

            # Print index and details to console
            print(f"Index: {index}")
            print(f"Company Name: {Company_Name}")
            print(f"Full Address: {Full_address}")
            print(f"Category: {Category}")
            print(f"Phone Number: {Phone_number}")
            print(f"Company Website: {Company_website}")
            print(f"Google Map URL: {Google_map_link}")
            print("-" * 50)

            # Write data to CSV file
            writer.writerow([Company_Name, Full_address, Category, Phone_number, Company_website,
                             Google_map_link])

            # Increment the index
            index += 1
        except Exception as e:
            print("Error:", e)
        sleep(2)

    # Close the CSV file after writing
    output_csv.close()

# Close the browser after all tasks
driver.quit()
