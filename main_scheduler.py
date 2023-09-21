# Env variables
import os

# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Time precision and waiting
import datetime
import pytz
import time

# Create test_mode
TEST_MODE = True

# Define the Pacific Time zone
pacific_timezone = pytz.timezone('US/Pacific')

# Define the start time for program
start_time = datetime.time(8, 56, 0)

if not TEST_MODE:
    while True:
        # Get the current time in Pacific Time
        current_time_pacific = datetime.datetime.now(pacific_timezone).time()

        # Check if start time is reached
        if current_time_pacific >= start_time:
            print(f"Time to start selenium: {current_time_pacific}")
            break

        # Print the current time for reference
        print(f"Current time in Pacific Time: {current_time_pacific}")

        # Sleep for 60 seconds before checking again
        time.sleep(60)


# Time to start program!

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

# Wait for schedule to go live at 9:00am
print("Waiting for schedule to go live at 9:00am")
print(f"Current time in Pacific Time: {datetime.datetime.now(pacific_timezone).time()}")
# Define the target time
target_time = datetime.time(9, 0, 0)

if not TEST_MODE:
    while True:
        # Get the current time in Pacific Time
        current_time_pacific = datetime.datetime.now(pacific_timezone).time()

        # Check if target time is reached
        if current_time_pacific >= target_time:
            print(f"Current time in Pacific Time: {current_time_pacific}")
            break

        # Wait
        time.sleep(0.5)

# Schedule is live!
# Wait half a second as extra precaution, then refresh the page
time.sleep(0.5)
driver.refresh()

# Temporary fix for time it takes page to load
while True:
    try:
        driver.find_element(By.ID, "cell99")
        print("Page loaded")
        break
    except:
        print("Page not loaded")
        time.sleep(.1)

# Page is loaded, time to book hours

# Hour slots of interest
CELL_LISTS = [
    [99, 78],
    [100, 79],
    [87, 94, 101],
    [88, 95, 102],
    [89, 96, 103],
    [106, 107, 108, 109, 110]
              ]

# Loop through list to attempt to schedule hours
for cell_list in CELL_LISTS:
    for cell_num in cell_list:
        # Select cell
        cell_id = f"cell{cell_num}"
        cell_box = driver.find_element(By.ID, cell_id)
        cell_box.click()

        # Schedule cell
        schedule_box = driver.find_element(By.ID, "butProviderSchedule")
        schedule_box.click()

        try:
            # Handles alert boxes that may pop up
            schedule_box.send_keys(Keys.ENTER)

        except:
            # Pop up alert did not appear, continue as normal
            continue

# Keep browser open for any necessary manual changes to be made
time.sleep(300)

# Close the browser window
driver.close()
print("Finished")
