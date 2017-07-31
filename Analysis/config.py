#! /usr/bin/env python
# -*- coding:utf-8 -*-

MONGO_CONFIG = {
    # configure MongoDB ip:port
    'MONGODB_SERVER': 'localhost',
    'MONGODB_PORT': '27017',
    # Configure MongoDB database & collections
    'MONGODB_DB_AUTOHOME': 'autohome_no_login',
    'MONGODB_COLLECTION_ARTICLE_SHORT': 'article_short',
    'MONGODB_COLLECTION_ARTICLE': 'article',
    'MONGODB_COLLECTION_COMMENT': 'comment',
    'MONGODB_COLLECTION_USER': 'user'
}

MONGO_SQL = {
    # 统计类的mongo_sql pipeline
    'statistics': {
        'editor_article_count': [
            {'$group': {'_id': '$article_writer', 'article_num': {'$sum': 1}}},
            {'$sort': {'article_num': -1}}
        ],
        'editor_comment_count': [
            {'$group': {'_id': '$article_writer', 'article_num': {'$sum': '$article_comment_num'}}},
            {'$sort': {'article_num': -1}}
        ]
    },
    'test': {
        'test_1': 'test'
    }
}
