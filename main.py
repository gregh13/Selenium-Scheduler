# Imports
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set the strategy to eager (doesn't wait for pictures to load)
options = Options()
options.page_load_strategy = 'eager'

# Create a Firefox WebDriver instance
driver = webdriver.Chrome()

# Navigate to tutor.com website
driver.get("https://www.tutor.com/")

# Sign in
sign_in_box = driver.find_element(By.CLASS_NAME, "signing-me-in")
sign_in_box.click()

# Test program up to this point
email_box = driver.find_element(By.ID, "userNameOrEmailAddress")
print("Email box object test: ", email_box)
time.sleep(2)
email_box.click()
time.sleep(2)
email_box.send_keys("MyEmail")
time.sleep(2)

# Close the browser window
driver.close()
print("Finished")
