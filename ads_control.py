import time
import requests


class AdsAPI:
    def __init__(self):
        self.basic_url = 'http://local.adspower.com:50325'

    def get_profiles(self):
        r = []
        for i in range(6):
            response = requests.get(f'{self.basic_url}/api/v1/user/list?page={i+1}&page_size=50').json()['data']['list']
            if response == []:
                break
            r.extend(response)
            time.sleep(1)
        return r

    def start_profile(self, profile_id):
        r = requests.get(f'{self.basic_url}/api/v1/browser/start?user_id={profile_id}').json()
        return r['data']['ws']['selenium']

    def stop_profile(self, profile_id):
        return requests.get(f'{self.basic_url}/api/v1/browser/stop?user_id={profile_id}').status_code
