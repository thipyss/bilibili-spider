import math
import time

import requests
import bv2av
from decode import Decode


def get_comments(bv: str):
    av = bv2av.dec(bv)
    url = "https://api.bilibili.com/x/v2/reply/count?type={}&oid={}".format(1, av)
    while True:
        try:
            data = requests.get(url).json()
            count = data['data']['count']
            break
        except KeyError:
            print('fail to get comments count, retrying...')
            time.sleep(1)
    pages = math.ceil(count / 20)
    for page in range(pages):
        params = {
            'type': 1,
            'oid': av
        }
        decoder = Decode(params)
        query = decoder.decode()
        print(query)

        url = "https://api.bilibili.com/x/v2/reply/wbi/main?" + query
        while True:
            try:
                data = requests.get(url).json()
                print(data)
                replies = data['data']['replies']
                break
            except KeyError:
                print('fail to get comments, retrying...')
                time.sleep(1)
        for reply in replies:
            comment = reply['content']['message']
            print(comment)

get_comments('BV1PN4y1U7fp')
