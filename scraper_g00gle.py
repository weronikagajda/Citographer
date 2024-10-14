from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import bs4
import os
import requests
import pandas as pd
from urllib3.exceptions import InsecureRequestWarning
import warnings

warnings.simplefilter('ignore', InsecureRequestWarning)

folder_name = 'your term' # ADJUST
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

def download_image(url, folder_name, file_name):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(os.path.join(folder_name, file_name + ".jpg"), 'wb') as file:
            file.write(response.content)

image_data_list = []

chromeDriverPath = r"C:\...\chromedriver.exe" # ADJUST
chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Adjust this path if needed

service = Service(executable_path=chromeDriverPath)

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument('--user-data-dir=C:/Users/.../AppData/Local/Google/Chrome/User Data/Default')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(service=service, options=chrome_options)

search_URL = "copy paste here the search result from google on chrome" # ADJUST
driver.get(search_URL)

time.sleep(40)

driver.execute_script("window.scrollTo(0, 0);")

page_html = driver.page_source

pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')

# Find image containers
containers = pageSoup.findAll('div', {'class': "eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"})

# Check the number of containers found
len_containers = len(containers)
print("Found %s image containers" % len_containers)

# Initialize a counter 
image_count = 0
max_images = 600  # ADJUST Set the maximum number of images to download

for i in range(1, len_containers + 1):
    if image_count >= max_images:
        break

    # Skip every 25th image
    if i % 25 == 0:
        continue

    try:
        xPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]""" % i
        driver.find_element(By.XPATH, xPath).click()

        timeStarted = time.time()
        while True:
            imageElement = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img""")
            imageURL = imageElement.get_attribute('src')
            imageAlt = imageElement.get_attribute('alt')

            if imageURL and imageURL.startswith("http"):
                break
            else:
                currentTime = time.time()
                if currentTime - timeStarted > 15:
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    break

        # Downloading image
        image_name = f"{folder_name}_{image_count + 1}"  
        download_image(imageURL, folder_name, image_name)
        image_data_list.append({'Image Name': image_name, 'SRC': imageURL, 'ALT': imageAlt})
        image_count += 1
        print(f"Downloaded image {image_name}. URL: {imageURL}")

    except Exception as e:
        print(f"Couldn't download image {i}, error: {e}. Continuing to the next one.")
        continue

image_data = pd.DataFrame(image_data_list)

csv_file_name = f"{folder_name}/image_details.csv"
image_data.to_csv(csv_file_name, index=False)
print(f"Saved image details to {csv_file_name}")

# Close the browser
driver.quit()
