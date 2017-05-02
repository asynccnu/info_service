# -*- coding: utf-8 -*-
import os
from datetime import timedelta


class Config(object):
    CELERY_BROKER_URL = 'redis://@{host}:7383/0'.format(host=os.getenv('BROKER_HOST'))  # celery消息代理, redis3容器
    CELERY_RESULT_BACKEND = 'redis://@{host}:7383/0'.format(host=os.getenv('BROKER_HOST')) # celery消息存储, redis3容器
    CELERYBEAT_SCHEDULE = {  # celery beat 定时任务
            'restart_redis_every_86400s': {
                # 每隔1天爬取通知公告
                'task': 'cute_board_spider',
                'schedule': timedelta(seconds=12*3600)
            },
    }


config = {
    'default': Config
}
