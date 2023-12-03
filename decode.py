import time
import urllib
from hashlib import md5
from functools import reduce
from urllib import parse

import requests

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


class Decode:
    def __init__(self, params: dict):
        self.params = params
        self.w_rid = ''
        self.wts = ''
        self.salt = ''

    def get_salt(self):
        url = 'https://api.bilibili.com/x/web-interface/nav'
        img_key = ''
        sub_key = ''
        response = requests.get(url)
        try:
            img_key = response.json()['data']['wbi_img']['img_url'].split('/')[-1].replace('.png', '')
            sub_key = response.json()['data']['wbi_img']['sub_url'].split('/')[-1].replace('.png', '')
        except:
            print('Failed to get key, retrying...')
            return
        key = img_key + sub_key
        self.salt = reduce(lambda x, y: x + key[y], mixinKeyEncTab, '')[:32]

    def decode(self):
        while self.salt == '':
            self.get_salt()
        cur_time = round(time.time())
        self.params['wts'] = str(cur_time)
        self.params = dict(sorted(self.params.items()))
        params = {
            k: ''.join(filter(lambda cha: cha not in "!'()*", str(v)))
            for k, v
            in self.params.items()
        }
        query = parse.urlencode(params)
        w_rid = md5((query + self.salt).encode()).hexdigest()
        params['w_rid'] = w_rid
        return urllib.parse.urlencode(params)
