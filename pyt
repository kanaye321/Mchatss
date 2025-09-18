# auto_login_and_go.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import getpass
import time

# ------------------ CONFIGURE ------------------
login_url = "https://example.com/login"        # page with login form
target_url = "https://example.com/some/page"   # destination AFTER login

# Replace these with the real identifiers from the site:
#  - if input has id attribute use (By.ID, "theId")
#  - if name attribute use (By.NAME, "theName")
#  - you can also use xpath or css selectors
username_locator = (By.ID, "username")   # example: (By.NAME, "username")
password_locator = (By.ID, "password")   # example: (By.NAME, "passwd")
submit_locator   = (By.XPATH, "//button[@type='submit']")  # adjust if needed
# ------------------------------------------------

# Get credentials securely: prefer env vars, otherwise prompt
username = os.getenv("AUTO_LOGIN_USER")
password = os.getenv("AUTO_LOGIN_PASS")
if not username:
    username = input("Username: ")
if not password:
    password = getpass.getpass("Password: ")

# Setup Chrome driver (non-headless so you can watch; set options for headless if needed)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # uncomment if you need headless
options.add_argument("--start-maximized")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

try:
    driver.get(login_url)

    wait = WebDriverWait(driver, 15)

    # Wait for username field and fill
    wait.until(EC.presence_of_element_located(username_locator))
    el_user = driver.find_element(*username_locator)
    el_user.clear()
    el_user.send_keys(username)

    # Wait for password field and fill
    wait.until(EC.presence_of_element_located(password_locator))
    el_pass = driver.find_element(*password_locator)
    el_pass.clear()
    el_pass.send_keys(password)

    # Click submit (or send Enter)
    wait.until(EC.element_to_be_clickable(submit_locator))
    driver.find_element(*submit_locator).click()

    # Wait for login to succeed — choose a reliable post-login condition.
    # Option A: wait for URL to change or a known element on the logged-in page.
    # Example: wait until target_url becomes accessible, or wait for a dashboard element:
    time.sleep(1)  # tiny pause before waiting for next condition

    # Example: wait for URL not to be the login page (simple heuristic)
    wait.until(lambda d: d.current_url != login_url)

    # Now navigate to your specific url (if login doesn't auto-redirect)
    driver.get(target_url)

    # Optional: wait for some element on the target page
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".chatbox")))

    print("Reached target URL:", driver.current_url)
    # keep browser open for a while so you can see results; remove or change as needed
    time.sleep(8)

finally:
    driver.quit()
