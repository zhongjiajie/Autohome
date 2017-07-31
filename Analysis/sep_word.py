#! /usr/bin/env python
# -*- coding:utf-8 -*-

import jieba
import pandas as pd
from pymongo import MongoClient

client = MongoClient('172.25.115.100', 27017)
db = client.autohome_no_login
collection = db.article
data = pd.DataFrame(list(collection.find()))

user_dict = 'user_dict.txt'
jieba.load_userdict(user_dict)
max_num = 7
curr = 0
for content in data.article_detail:
    curr += 1
    if curr == max_num:
        break
    else:
        print '/'.join(jieba.cut(content))


def tmp_function_to_fly(self, nice, *args):
    if args:
        pass
