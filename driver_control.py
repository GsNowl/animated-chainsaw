from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

from ads_control import AdsAPI
from logger import logger


class Driver:
    def __init__(self, profile_id, version):
        try:
            url = AdsAPI().start_profile(profile_id)
            chrome_driver_path = Service(f'chromedriver{version}.exe')
            options = webdriver.ChromeOptions()
            options.debugger_address = url
            options.add_argument("start-maximized")

            # Запуск и ввод
            self.driver = webdriver.Chrome(service=chrome_driver_path, options=options)
            logger.info(f'START PROFILE {profile_id}')
        except Exception as ex:
            print(ex)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def open(self, url):
        self.driver.get(url)
        logger.info(f'GO TO {url}')

    def click(self, xpath):
        if self.check_exists_by_xpath(xpath):
            self.driver.find_element(By.XPATH, xpath).click()
            return True
        return False

    def click_by_index(self, xpath, index):
        if self.check_exists_by_xpath(xpath):
            self.driver.find_elements(By.XPATH, xpath)[index].click()
            return True
        return False

    def click_with_wait(self, xpath):
        while not self.check_exists_by_xpath(xpath):
            time.sleep(1)
        self.driver.find_element(By.XPATH, xpath).click()

    def send_keys(self, keys, xpath):
        if self.check_exists_by_xpath(xpath):
            self.driver.find_element(By.XPATH, xpath).send_keys(keys)
            return True
        return False

    def send_keys_by_index(self, keys, xpath, index):
        if self.check_exists_by_xpath(xpath):
            self.driver.find_elements(By.XPATH, xpath)[index].send_keys(keys)
            return True
        return False

    def send_keys_with_wait(self, keys, xpath):
        while not self.check_exists_by_xpath(xpath):
            time.sleep(1)
        self.driver.find_element(By.XPATH, xpath).send_keys(keys)

    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_window_by_index(self, index):
        self.driver.switch_to.window(self.driver.window_handles[index])
        logger.info(f'switch to {index} window')

    def close_all_windows(self):
        self.switch_to_new_window()
        while len(self.driver.window_handles) > 1:
            self.driver.close()
            self.switch_to_new_window()
            time.sleep(1)
