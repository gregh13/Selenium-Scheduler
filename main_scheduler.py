# Env variables
import os

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options

# Time precision and waiting
import datetime
import pytz
import time

# Used to make output & log files easier to read
LINEBREAK = "-------------------------------------------------"

# Initialize Test Mode
TEST_MODE = False

# Give user option to run in Test Mode
mode_input = input("Run in Test Mode? Type y/n: ")
if mode_input == 'y':
    TEST_MODE = True

# Define the Pacific Time zone
pacific_timezone = pytz.timezone('US/Pacific')

# Get date for log file
date = datetime.date.today()

# Define the start time for program
start_time = datetime.time(8, 55, 0)

# Define default log file
filename = f"schedule-log-{date}.txt"

# Save to test log when in Test Mode
if TEST_MODE:
    filename = "test_log.txt"

# Useful to user
print(f"\nLog will be saved to {filename}\n")

# Begin log process
log_file = open(filename, "w")

# Write log file header, centered according to Linebreak length
log_file.write(f"{LINEBREAK}\n           Selenium Hour Scheduler Log\n{LINEBREAK}\n\n")
print(f"{LINEBREAK}\n           Selenium Hour Scheduler Log\n{LINEBREAK}\n")

# While loop with longer sleep period when time to schedule hours is further away
if not TEST_MODE:

    # For improved output and logging
    log_file.write(f"Waiting until it's near {start_time} to schedule hours...\n")
    print(f"Waiting until it's near {start_time} to schedule hours...")

    while True:
        # Get the current time in Pacific Time
        current_time_pacific = datetime.datetime.now(pacific_timezone).time()

        # Check if start time is reached
        if current_time_pacific >= start_time and current_time_pacific.hour < 10:
            log_file.write(f"Time to start selenium: {current_time_pacific}\n")
            print(f"Time to start selenium: {current_time_pacific}")
            break

        # Print the current time for reference
        log_file.write(f"Current Pacific Time: {current_time_pacific}\n")
        print(f"Current Pacific Time: {current_time_pacific}")

        # Sleep for 60 seconds before checking again
        time.sleep(60)

# ---------------------
# Time to start program!

# Get ENV variables
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
WEBSITE = os.environ.get("WEBSITE")

# Set the strategy to eager (doesn't wait for pictures to load)
options = Options()
options.page_load_strategy = 'eager'

# Create a Chrome WebDriver instance
driver = webdriver.Chrome(options=options)

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

# Get current number of hours scheduled
current_hours = driver.find_element(By.ID, "lblScheduledHours").text
print(f"{LINEBREAK}\nCurrent number of hours scheduled: {current_hours}")
log_file.write(f"{LINEBREAK}\nCurrent number of hours scheduled: {current_hours}\n")

# Define the target time
target_time = datetime.time(9, 0, 0)

# Wait for schedule to go live at target time
log_file.write(f"Waiting for schedule to go live at {target_time}\n")
print(f"Waiting for schedule to go live at {target_time}")

log_file.write(f"Current Pacific Time: {datetime.datetime.now(pacific_timezone).time()}\n")
print(f"Current Pacific Time: {datetime.datetime.now(pacific_timezone).time()}")

if not TEST_MODE:
    while True:
        # Get the current time in Pacific Time
        current_time_pacific = datetime.datetime.now(pacific_timezone).time()

        # Check if target time is reached
        if current_time_pacific >= target_time:
            log_file.write(f"Current Pacific Time: {current_time_pacific}\n")
            print(f"Current Pacific Time: {current_time_pacific}")
            break

        # Wait
        time.sleep(0.5)

# -----------------
# Schedule is live!
# Wait half a second as extra precaution, then refresh the page
time.sleep(0.5)
driver.refresh()

# Waiting for page to load
driver.implicitly_wait(time_to_wait=10)

# Log process start
log_file.write(f"\nBegin scheduling\n-------------\n")
print(f"\nBegin scheduling\n-------------")


# Alert popup triggers vary greatly, create default alert handler
def try_alert(time_sleep: float = 0.1, retries: int = 1, attempt: int = 0):
    try:
        # Handles alert boxes that may pop up
        alert = Alert(driver)
        alert_text = alert.text
        alert.accept()
        log_file.write(f"Pop up appeared for cell {cell_num}--> {alert_text}\n")
        print(f"Pop up appeared for cell {cell_num}--> {alert_text}")
        return
    except:
        # Pop up alert did not appear, continue as normal
        pass

    if attempt < retries:
        time.sleep(time_sleep)
        try_alert(time_sleep, retries, attempt+1)

    return


# Original slots of interest
# CELL_LISTS = [
#     [99, 78],
#     [100, 79],
#     [87, 94, 101],
#     [88, 95, 102],
#     [89, 96, 103],
#     [106, 107, 108, 109, 110]
#               ]

# Current Cell List
CELL_LISTS = [
    [88, 95, 102],
    [100, 101],
    [89, 96, 103],
    [109, 110]
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

        # Protect against alert messages
        try_alert(time_sleep=0.1, retries=1, attempt=0)

# Log update
log_file.write("-------------\nFinished scheduling\n")
print("-------------\nFinished scheduling")

# Check updated hours scheduled
updated_hours = driver.find_element(By.ID, "lblScheduledHours").text

# Log before and after hour comparison
print(f"{LINEBREAK}\nPrevious number of hours scheduled: {current_hours}")
log_file.write(f"{LINEBREAK}\nPrevious number of hours scheduled: {current_hours}\n")

print(f"Updated number of hours scheduled: {updated_hours}")
log_file.write(f"Updated number of hours scheduled: {updated_hours}\n")

# Calculate & output number of new hours added
print(f"Hours added: {int(updated_hours) - int(current_hours)}\n")
log_file.write(f"Hours added: {int(updated_hours) - int(current_hours)}\n")

# Keep browser open for any necessary manual changes to be made
time.sleep(600)

# Close the browser window
driver.close()
log_file.write("Driver closed\n")
print("Driver closed")

log_file.close()
