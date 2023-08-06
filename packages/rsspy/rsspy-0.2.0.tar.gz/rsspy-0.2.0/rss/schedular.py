import socket
import threading
import time
from enum import Enum
from sched import scheduler

import codefast as cf
from codefast.concurrent.scheduler import BackgroundScheduler
from ojbk import report_self

from rss.apps.freeapp import publish_feeds
from rss.apps.huggingface import HuggingFace
from rss.apps.leiphone import LeiPhoneAI
from rss.apps.pingwest import PingWest
from rss.apps.rsshub import RssHub
from rss.apps.rust import RustLangDoc
from rss.base.wechat_public import create_rss_worker
from rss.base.wechat_rss import create_rss_worker as create_wechat_rss_worker
from rss.core.tg import tcp
from rss.tracker import main as blog_main

socket.setdefaulttimeout(300)


class PostType(str, Enum):
    """
    PostType
    """
    IMMEDIATE = 'immediate'
    EVENING8 = 'evening8'


class Schedular(object):
    def __init__(self):
        """Add disturb to avoid multiple updates posted at exactly the same time
        Args:
            post_type(PostType): whether to post immediately or delay at a certain time, e.g., 20:00 pm
        """
        self.timer = 0
        self.articles_stack = []

    def run(self):
        cf.info("schedular: %s is running" % self.__class__.__name__)
        self.action()

    def run_worker(self, worker):
        latest = worker.pipeline()
        if not latest:
            cf.info('no new articles for {}'.format(worker.__class__.__name__))
        else:
            worker.save_to_redis(latest)
            cf.info('all articles saved to redis')
            self.articles_stack = []
            for article in latest:
                cf.info(article)
                tcp.post(article.telegram_format())


class DailyBlogTracker(Schedular):
    def __init__(self):
        super().__init__()

    def action(self):
        cf.info("DailyBlogTracker is running")
        blog_main()


class LeiPhoneAIRss(Schedular):
    def action(self):
        self.run_worker(LeiPhoneAI())


class HuggingFaceRss(Schedular):
    def action(self):
        self.run_worker(HuggingFace())


class RustLanguageDoc(Schedular):
    def action(self):
        self.run_worker(RustLangDoc())


class WechatPublicRss(Schedular):
    def __init__(self, wechat_id: str = 'almosthuman'):
        super().__init__()
        self.worker = create_rss_worker(wechat_id)

    def action(self):
        self.run_worker(self.worker)


class WechatRssMonitor(Schedular):
    def __init__(self, wechat_id: str = 'almosthuman'):
        super().__init__()
        self.worker = create_wechat_rss_worker(wechat_id)

    def action(self):
        self.run_worker(self.worker)


class SchedularManager(object):
    def __init__(self):
        self.schedulars = []
        self.timer = 0

    def add_schedular(self, schedular) -> Schedular:
        self.schedulars.append(schedular)
        return self

    def run_once(self):
        for schedular in self.schedulars:
            try:
                threading.Thread(target=schedular.run).start()
            except Exception as e:
                cf.error('shcedular {} error: {}'.format(schedular, e))

    def run(self):
        cf.info('schedular manager is running')
        self.run_once()


class PingWestRss(Schedular):
    def action(self):
        self.run_worker(PingWest())


class RssHubRss(Schedular):
    def action(self):
        self.run_worker(RssHub())


def rsspy():
    manager = SchedularManager()
    manager.add_schedular(LeiPhoneAIRss())
    manager.add_schedular(HuggingFaceRss())
    manager.add_schedular(PingWestRss())
    manager.add_schedular(RssHubRss())
    # manager.add_schedular(DailyBlogTracker())
    manager.add_schedular(WechatPublicRss(wechat_id='huxiu'))

    wechat_ids = [
        'almosthuman', 'yuntoutiao', 'aifront', 'rgznnds', 'infoq', 'geekpark',
        'qqtech'
    ]
    for wechat_id in wechat_ids:
        manager.add_schedular(WechatRssMonitor(wechat_id))

    try:
        manager.run()
        report_self('RSS')
    except Exception as e:
        cf.error('rsspy run failure', e)


if __name__ == '__main__':
    s1 = BackgroundScheduler(trigger='interval', interval=60)
    s1.add_job(publish_feeds)
    s1.start()
    s2 = BackgroundScheduler(trigger='cron', hour='8-20', minute='*/7')
    s2.add_job(rsspy)
    s2.start()
    cf.info('rss scheduler started')

    while True:
        time.sleep(1)
