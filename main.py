import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TWITTER_EMAIL = ''
TWITTER_HANDLE = ""
TWITTER_PASS = ''
QUOTED_UP_SPEED = 73
QUOTED_DOWN_SPEED = 18
CHROME_DRIVER_PATH = "/Users/adam/Development/chromedriver"
SPEED_TEST_URL = 'https://www.speedtest.net'
TWITTER_URL = "https://x.com/"


class InternetSpeedTwitterBot:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)  # Option to keep Chrome open
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)
        #Clear Cookie Pop-Up
        try:
            reject_cookies_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler')))
            reject_cookies_btn.click()
        except NoSuchElementException:
            print("No Cookie Pop-up")
        #Start Speed Test
        try:
            start_speed_test_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[tabindex="3"]')))
            start_speed_test_btn.click()
        except NoSuchElementException:
            print("Cannot Find Go Button")
        #Wait for speed test to finish and get values
        try:
            time.sleep(90)
            upload_speed_tag = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "upload-speed")))
            download_speed_tag = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "download-speed")))
            self.up = float(upload_speed_tag.text)
            self.down = float(download_speed_tag.text)
            print(self.up, self.down)
        except NoSuchElementException:
            print("Cannot find wifi speeds")

        self.driver.quit()

    def tweet_at_provider(self, message):
        self.driver.get(TWITTER_URL)
        #Reject Cookie Pop-up
        try:
            reject_cookies_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/button[2]')))
            reject_cookies_btn.click()
        except NoSuchElementException:
            print("No Cookie Pop-up")
        #Click login to twitter
        try:
            login_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="loginButton"]')))
            login_btn.click()
        except NoSuchElementException:
            print("Failed to login.")
        #Fill details
        try:
            email_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="username"]')))
            email_input.send_keys(TWITTER_EMAIL)
            next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')))
            next_btn.click()
            user_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"]')))
            user_input.send_keys(TWITTER_HANDLE)
            user_input.send_keys(Keys.ENTER)
            pass_input = self.wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
            pass_input.send_keys(TWITTER_PASS, Keys.ENTER)

        except NoSuchElementException:
            print("Failed to login.")

        #Write Tweet NB: Add try for if security pop up comes up
        try:
            tweet_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
            tweet_input.send_keys(message)
        except:
            print("Couldn't write Tweet")


internet_speed_bot = InternetSpeedTwitterBot()
internet_speed_bot.get_internet_speed()
if internet_speed_bot.up < QUOTED_UP_SPEED or internet_speed_bot.down < QUOTED_DOWN_SPEED:
    message= (f"Hey Internet Provider, why is my internet speed "
              f"{internet_speed_bot.up}up/ {internet_speed_bot.down}down "
              f"when I pay for {QUOTED_UP_SPEED}up/ {QUOTED_DOWN_SPEED}down?!")
    internet_speed_bot.tweet_at_provider(message)
