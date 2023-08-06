#!/usr/bin/env python
""" 品玩 rss 数据抓取 
"""
from typing import List
import feedparser

from rss.base.anynews import AnyNews, Article


class PingWest(AnyNews):
    def __init__(self):
        main_url = 'https://rsshub.app/pingwest/tag/%E7%A1%85%E6%98%9F%E4%BA%BA/1'
        super().__init__(main_url)
        self.type += ':pintwest'

    def search_articles(self, _soup) -> List[Article]:
        """ search articles in the soup
        """
        return [
            Article(uid=feed.id,
                    title=feed.title,
                    url=feed.link,
                    source="",
                    author=feed.author,
                    date=feed.published,
                    extra_url=feed.link)
            for feed in feedparser.parse(self.main_url).entries
        ]


