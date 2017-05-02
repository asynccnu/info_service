# -*- coding: utf-8 -*-
import os
from service import app, make_celery
from service.api import webview_board
from service.spider import get_webview_board
from werkzeug.exceptions import InternalServerError


celery = make_celery(app)


@celery.task(name='cute_board_spider')
def cute_board_spider():
    """
    :function: cute_board_spider

    每隔一天清空通知公告爬虫缓存
    """
    try:
        webview_board_list = get_webview_board()
    except:
        raise InternalServerError()
    webview_board.flushdb()
    webview_board.set('webview_board_list', webview_board_list)
    webview_board.save()
