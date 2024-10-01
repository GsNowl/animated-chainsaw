import time
from logger import logger
from driver_control import Driver
from config import *

from selenium.webdriver.common.keys import Keys


class RubbyWallet:
    def __init__(self, driver, profile_id):
        self.driver: Driver = driver
        self.profile_id = profile_id
        self.mnemonic = profiles[profile_id]

    def import_mnemonic(self):
        self.driver.switch_to_window_by_index(0)
        while self.driver.driver.current_url == 'chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/offscreen.html':
            self.driver.driver.close()
            self.driver.switch_to_window_by_index(0)
        self.driver.open('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/import/mnemonics')
        time.sleep(2)
        if self.driver.driver.current_url != 'chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/import/mnemonics':
            if self.driver.click('//button[@class="ant-btn ant-btn-primary ant-btn-lg ant-btn-block"]'):
                logger.debug('click NEXT')
                time.sleep(0.3)

            if self.driver.click('//button[@class="ant-btn ant-btn-primary ant-btn-lg ant-btn-block"]'):
                logger.debug('click GET STARTED')
                time.sleep(0.3)

            self.driver.click('//div[text()="Import Seed Phrase"]')
            logger.info('click "Import Seed Phrase"')
            time.sleep(2)

            for i in range(2):
                self.driver.send_keys_by_index(password, '//input[@type="password"]', i)
                logger.info(f'insert {password}')

            self.driver.click('//button[@type="submit"]')
            logger.info('click Submit')

            time.sleep(1)

            return self.import_mnemonic()

        for i, j in zip(range(12), self.mnemonic.split(' ')):
            self.driver.send_keys_by_index(j, '//input[@type="password"]', i)
            logger.debug(f'insert {j}')
        time.sleep(0.5)
        self.driver.click('//button[@type="submit"]')
        logger.debug('click "confirm"')
        self.driver.click_with_wait('//button[@class="ant-switch AddToRabby"]')
        logger.debug('turn on first address in list')
        self.driver.click_by_index('//button[@type="button"]', -1)
        logger.debug('click "DONE"')

        time.sleep(2)
