import json
import os
from conf import settings


def select(username):
    user_path = os.path.join(settings.USER_DATA_PATH, f'{username}.json')
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf8') as f:
            user_dic = json.load(f)
            return user_dic


def save(user_dic):
    username = user_dic.get('username')
    user_path = os.path.join(settings.USER_DATA_PATH, f'{username}.json')
    with open(user_path, 'w', encoding='utf8') as f:
        json.dump(user_dic, f, ensure_ascii=False)



def select_shop():
    user_path = os.path.join(settings.SHOP_CAR_DATA_PATH, f'shop_mall.json')
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf8') as f:
            shop_list = json.load(f)
            return shop_list


def save_shop(shop_list):
    # username = user_dic.get('username')
    user_path = os.path.join(settings.SHOP_CAR_DATA_PATH, f'shop_mall.json')
    with open(user_path, 'w', encoding='utf8') as f:
        json.dump(shop_list, f, ensure_ascii=False)
