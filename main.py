from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 7)

        print('opening instagram')
        self.driver.get("https://instagram.com")
        self.wait_find_click("//a[contains(text(), 'Log in')]")

        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        print('logging in..')
        self.wait_find_click("//button[contains(text(), 'Not Now')]")

    def get_unfollowers(self):
        sleep(1)
        print('open personal profile')
        self.driver.find_element_by_xpath(f"//a[contains(@href,'/{self.driver.find_element_by_xpath('//input[@name=\"username\"]').get_attribute('value')}')]").click()
        self.is_element_exist("//a[contains(@href,'/following')]")
        print('opening following tab')
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        print('scanning following users')
        following = self._get_users()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        print('scanning followers')
        followers = self._get_users()
        not_following_back = [user for user in following if user not in followers]
        print('===Users not following back...====')
        print(not_following_back)

    def _get_users(self):
        sleep(3)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_height, height = 0, 1
        scroll = 0
        print("scrolling", end='', flush=True)
        while last_height != height:
            last_height = height
            print(".", end='', flush=True)
            sleep(1)
            scroll += 1
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
            """, scroll_box)
        print('scrolled ', scroll, 'times')
        print('making a list...')
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

    def wait_find_click(self, xpath_text):
        elements = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath_text)))
        return self.driver.find_element_by_xpath(xpath_text).click() if elements else False

    def is_element_exist(self, xpath_text):
        elements = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath_text)))
        return None if elements else False
