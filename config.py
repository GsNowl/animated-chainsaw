import json

completed_profiles = ['jd2uayd']
password = 'zaebalsya_na_starte1'
version_ = 120
from_json = True  # or True ДОСТАВАТЬ ФАЙЛЫ ИЗ ФАЙЛА (True) или по порядку, как в адс (False)
need_import_mnemonic = True

profiles = dict()
with open("profiles.json", 'r') as file:
    profiles = dict(json.load(file))
