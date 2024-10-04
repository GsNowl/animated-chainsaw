import json

completed_profiles = []
password = 'zaebalsya_na_starte1'
version_ = 120
from_json = True  # or True ДОСТАВАТЬ ФАЙЛЫ ИЗ ФАЙЛА (True) или по порядку, как в адс (False)

profiles = dict()
with open("profiles.json", 'r') as file:
    profiles = dict(json.load(file))
