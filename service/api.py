# -*- coding: utf-8 -*-

import os
import re
import ast
import json
import redis
from flask import request, jsonify, Blueprint, redirect, url_for
from spider import get_webview_board

api = Blueprint(
        'api',
        __name__,
        )

webview_board = redis.StrictRedis(host=os.getenv('WEBVIEW_REDIS_HOST'), port=7388, db=0)
cleanr = re.compile('<.*?>')

@api.route('/webview_info/')
def api_webview_info():
    """
    :function: webview_info
    :args: none
    :rv: all board with format

    返回带有格式的通知公告(3个平台每个平台5个)
    """
    webview_board_list = webview_board.get('webview_board_list')
    if not webview_board_list:
        board_list = get_webview_board()
        webview_board.set('webview_board_list', board_list)
    all_board = ast.literal_eval(webview_board.get('webview_board_list'))
    return jsonify(all_board), 200

@api.route('/info/')
def api_info():
    webview_board_list = webview_board.get('webview_board_list')
    if not webview_board_list:
        board_list = get_webview_board()
        webview_board.set('webview_board_list', board_list)
    all_board = ast.literal_eval(webview_board.get('webview_board_list'))
    # convert html to plain text
    for item in all_board:
        item['content'] = re.sub(cleanr, '', item['content'])
    return jsonify(all_board), 200
