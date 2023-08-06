#!/usr/bin/env python
""" 品玩 rss 数据抓取 
"""
from typing import List

import feedparser

from rss.base.anynews import AnyNews, Article


class RssHub(AnyNews):
    def __init__(self):
        main_url = 'http://abehiroshi.la.coocan.jp/'
        super().__init__(main_url)
        self.type += ':rsshub'
        self.urls = [
            'https://rsshub.app/infoq/recommend',  # infoq 推荐
            'https://rsshub.app/geektime/column/48',  # geektime 
            'https://rsshub.app/juejin/category/ai',  # juejin AI
            'https://rsshub.app/meituan/tech/home',  # 美团技术
            'https://rsshub.app/blogs/paulgraham', # Paul Graham
            'https://www.msra.cn/feed', #msra deepl articles
        ]

    def search_articles(self, _soup) -> List[Article]:
        """ search articles in the soup
        """
        articles = []
        for url in self.urls:
            articles.extend([
                Article(uid=feed.id,
                        title=feed.title,
                        url=feed.link,
                        source="",
                        author=feed.author if 'author' in feed else '',
                        date=feed.published if 'published' in feed else '',
                        extra_url=feed.link)
                for feed in feedparser.parse(url).entries
            ])
        return articles
