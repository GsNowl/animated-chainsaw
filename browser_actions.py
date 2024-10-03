import random
import time

from selenium.common import ElementClickInterceptedException

from logger import logger
from driver_control import Driver
from config import *

from selenium.webdriver.common.keys import Keys


class InitDriver:
    def __init__(self, driver, profile_id):
        self.driver: Driver = driver
        self.profile_id = profile_id
        logger.info('Init profile for work')


class RabbyWallet(InitDriver):
    def import_mnemonic(self):
        mnemonic = profiles[self.profile_id]
        self.driver.switch_to_window_by_index(0)
        while self.driver.driver.current_url == 'chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/offscreen.html':
            self.driver.driver.close()
            self.driver.switch_to_window_by_index(0)
        self.driver.open('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/import/mnemonics', 2)
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

        for i, j in zip(range(12), mnemonic.split(' ')):
            self.driver.send_keys_by_index(j, '//input[@type="password"]', i)
            logger.debug(f'insert {j}')
        time.sleep(0.5)
        self.driver.click('//button[@type="submit"]')
        logger.debug('click "confirm"')
        self.driver.click_with_wait('//button[@class="ant-switch AddToRabby"]')
        logger.debug('turn on first address in list')
        self.driver.click_by_index('//button[@type="button"]', -1)
        logger.debug('click "DONE"')
        logger.info('Rubby waller is imported')

        time.sleep(2)

    def login(self):
        self.driver.open('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/unlock')
        self.driver.send_keys([password, Keys.ENTER], '//input[@type="password"]')
        logger.info('Log in Rabby Wallet')

    def flip(self):
        self.driver.open('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/dashboard', 2)
        self.driver.click_with_wait('//div[@class="rabby-default-wallet-setting is-metamask"]/a')
        logger.debug('Click on Flip')

    def connect(self):
        self.driver.switch_to_last()
        time.sleep(4)
        while True:
            try:
                self.driver.click('//button[@class="ant-btn ant-btn-primary ant-btn-lg mb-0"]')
                logger.info('Click on Connect')
                break
            except ElementClickInterceptedException:
                if self.driver.click('//span[text()="Ignore all"]'):
                    logger.info('Click on Ignore all')
                    time.sleep(2)
        time.sleep(1)

    def sign(self):
        self.driver.switch_to_last()
        self.driver.click_with_wait('//button/span[text()="Sign"]')
        logger.info('Click on Sign')
        self.driver.click_with_wait('//button[text()="Confirm"]')
        logger.info('Click on Confirm')
        time.sleep(3)
        self.driver.switch_to_last()


class SonicLabs(InitDriver):
    rabby: RabbyWallet = None

    def connect(self):
        self.driver.open('https://arcade.soniclabs.com/', 5)

        if not self.driver.click('//span[text()="Connect Wallet"]'):
            logger.info('Rabby is already connected to site')
            return

        logger.debug('Click on Connect Wallet')
        self.driver.click('//button[text()="Rabby"]')
        logger.debug('Click on Rabby')
        time.sleep(1)
        if self.driver.check_exists_by_xpath('//div[text()="Selected wallet provider is not found."]'):
            self.rabby.flip()
            return self.connect()

        self.rabby.connect()
        logger.info('Rabby is connected to site')

    def is_needed_sign(self, len_windows, func):
        if len_windows != len(self.driver.driver.window_handles):
            self.rabby.sign()
            return func()

    def plinko(self):
        self.driver.open('https://arcade.soniclabs.com/game/plinko', 2)
        if self.driver.get_text('//span[@class="rounded-md bg-white/10 px-2 py-1 font-bold text-white"]') == '0 / 20':
            logger.info('Plinko completed')
            return True

        for _ in range(random.randint(5, 8)):
            try:
                self.driver.click_with_wait('//button[@type="submit"]')
                logger.info('Click on Play')
            except ElementClickInterceptedException:
                self.rabby.sign()

                return self.plinko()
            time.sleep(5)
        return self.plinko()

    def mines(self):
        self.driver.open('https://arcade.soniclabs.com/game/mines', 5)
        if self.driver.get_text('//span[@class="rounded-md bg-white/10 px-2 py-1 font-bold text-white"]') == '0 / 20':
            logger.info('Mines completed')
            return True

        mine_xpath = '//button[@class="wr-h-full wr-w-full"]'
        while not self.driver.check_exists_by_xpath(mine_xpath):
            logger.debug('Wait until exists Mine_Card')
            time.sleep(1)
        len_windows = len(self.driver.driver.window_handles)

        for i in range(0, random.randint(0, 7)):
            self.driver.click_by_index(mine_xpath, i)
            logger.debug('Click in Mine')
            time.sleep(0.1)

        time.sleep(2)
        self.is_needed_sign(len_windows, self.mines)

        # not ended

    def wheel(self):
        self.driver.open('https://arcade.soniclabs.com/game/wheel', 3)
        self.driver.click(f'//button[@value="{random.randint(1,4)}"]')
        logger.debug('Click on x btn')
        time.sleep(1)

        len_windows = len(self.driver.driver.window_handles)
        self.driver.click('//button[text()="Play"]')
        logger.debug('Click in Play')
        time.sleep(2)

        self.is_needed_sign(len_windows, self.wheel)

        # need to write to end
