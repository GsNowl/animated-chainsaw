import json

completed_profiles = ['jd2uayd', 'jd2u9hy', 'jd2uaxi', 'jd2u9gv', 'jd2u9gf', 'jd2u9fj', 'jd2u9eo', 'jd2u9dh', 'jd2u9cs', 'jd2u996', 'jd2uawo', 'jd2uate', 'jd2uaq6', 'jd2uapa', 'jd2uaor', 'jd2uanv', 'jd2uanf', 'jd2uajj', 'jd2uahg', 'jd2uagw', 'jd2uafn', 'jd2uaf2', 'jd2uaen', 'jd2uadr', 'jd2uada', 'jd2uacm', 'jd2uabv', 'jd2uab3', 'jd2uaah', 'jd2ua90', 'jd2ua88', 'jd2ua6n', 'jd2ua43', 'jd2ua1j', 'jd2ua0t', 'jd2ua05', 'jd2u9y0', 'jd2u9wv', 'jd2u9v8', 'jd2u9ug', 'jd2u9u1', 'jd2u9tb', 'jd2u9sp', 'jd2u9ry', 'jd2u9r7', 'jd2u9pg', 'jd2u9oc', 'jd2u9ns', 'jd2u9kl', 'jd2u9im']
password = 'zaebalsya_na_starte1'
version_ = 120
from_json = True  # or True ДОСТАВАТЬ ФАЙЛЫ ИЗ ФАЙЛА (True) или по порядку, как в адс (False)
need_import_mnemonic = True

profiles = dict()
with open("profiles.json", 'r') as file:
    profiles = dict(json.load(file))
