# Imports
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Get ENV variables
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
WEBSITE = os.environ.get("WEBSITE")

# Set the strategy to eager (doesn't wait for pictures to load)
# options = Options()
# options.page_load_strategy = 'eager'

# Create a Chrome WebDriver instance
driver = webdriver.Chrome()

# Navigate to website
driver.get(WEBSITE)

# Sign in
email_box = driver.find_element(By.ID, "txtUserName")
email_box.click()
email_box.send_keys(os.environ.get('EMAIL'))
time.sleep(1)

password_box = driver.find_element(By.ID, "txtPassword")
password_box.click()
password_box.send_keys(os.environ.get('PASSWORD'))
time.sleep(1)

submit_box = driver.find_element(By.ID, "butSignIn")
submit_box.click()
time.sleep(1)

# Navigate schedule
next_week_box = driver.find_element(By.NAME, "weekAhead")
next_week_box.click()
time.sleep(1)


CELL_LISTS = [
    [99, 78],
    [100, 79],
    [87, 94, 101],
    [88, 95, 102],
    [89, 96, 103],
    [106, 107, 108, 109, 110]
              ]

for cell_list in CELL_LISTS:
    for cell_num in cell_list:
        cell_id = f"cell{cell_num}"
        cell_box = driver.find_element(By.ID, cell_id)
        cell_box.click()
        schedule_box = driver.find_element(By.ID, "butProviderSchedule")
        schedule_box.click()

        try:
            # Handles alert boxes that may pop up
            schedule_box.send_keys("Return")
        except:
            # exception raised is "Element Not Interactable"
            continue

time.sleep(2)

# Close the browser window
driver.close()
print("Finished")
