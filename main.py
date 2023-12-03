import math
import time

import requests
import bv2av
from decode import Decode
import database


def get_comments(bv: str):
    res = []
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
            'oid': av,
            'next': page
        }
        decoder = Decode(params)
        query = decoder.decode()

        url = "https://api.bilibili.com/x/v2/reply/wbi/main?" + query
        while True:
            try:
                data = requests.get(url).json()
                replies = data['data']['replies']
                break
            except KeyError:
                print('fail to get comments, retrying...')
                time.sleep(1)
        for reply in replies:
            comment_id = reply['rpid']
            bv = bv
            uid = reply['member']['mid']
            likes = reply['like']
            ip = reply['reply_control']['location'] if 'location' in reply['reply_control'] else ''
            publish_time = reply['ctime']
            root_id = reply['root']
            parent_id = reply['parent']
            content = reply['content']['message']
            data = {
                'comment_id': comment_id,
                'bv': bv,
                'uid': uid,
                'likes': likes,
                'ip': ip,
                'publish_time': publish_time,
                'root_id': root_id,
                'parent_id': parent_id,
                'content': content
            }
            print(content)
            res.append(data)
    Database = database.Database()
    Database.create_table('comments')
    Database.multi_insert('comments', res)
    Database.close()

get_comments('BV1PN4y1U7fp')
