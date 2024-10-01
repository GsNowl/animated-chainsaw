import time
import os

from ads_control import AdsAPI
from driver_control import Driver
from browser_actions import RubbyWallet
from config import completed_profiles, version_, from_json, profiles
from logger import logger


def rewrite_completed_profiles():
    config_file = os.path.basename('config.py')
    with open(config_file, 'r', encoding='utf-8') as file:
        text = file.read().split('\n')
        for j, i in enumerate(text):
            if i.startswith('completed_profiles = ['):
                text[j] = f'completed_profiles = {completed_profiles}'

    with open(config_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(text))


def main(profiles_dict):
    if from_json:
        profiles_dict = [i for i in profiles_dict if i not in completed_profiles]
    else:
        profiles_dict = [i['user_id'] for i in AdsAPI().get_profiles() if i['user_id'] not in completed_profiles]
    for i in profiles_dict:
        driver = Driver(i, version_)
        time.sleep(1.5)
        # driver.close_all_windows()
        print(driver.driver.current_url)
        rubby = RubbyWallet(driver, i)
        rubby.import_mnemonic()
        logger.info('Rubby waller is imported')

        # time.sleep(12321)

        AdsAPI().stop_profile(i)
        completed_profiles.append(i)
        rewrite_completed_profiles()


if __name__ == '__main__':
    main(profiles)
