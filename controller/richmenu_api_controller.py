from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
import requests
import json
from lib.db import Database
import psycopg2.extras
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


class RichmenuApiRelateController(Resource):
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_TOKEN'))
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET_KEY'))

    def post(self):
        usage = request.args.get('usage')
        if usage == 'create':
            rich_menu_to_create = RichMenu(
                size=RichMenuSize(width=2500, height=843),
                selected=False,
                name="Nice richmenu",  # display name
                chat_bar_text="我是測試使用",
                areas=[RichMenuArea(  # 這邊是陣列的格式，可以動態設定自己要的區域想要有什麼功能
                    bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                    action=URIAction(label='Go to line.me', uri='https://line.me'))]
            )
            rich_menu_id = self.line_bot_api.create_rich_menu(
                rich_menu=rich_menu_to_create)
            print(rich_menu_id)
            return {'id': rich_menu_id}, 200
        elif usage == 'upload':
            file = request.files['the_file'].read()
            rich_menu_id = request.form['richmenu_id']
            content_type = "image/png"
            try:
                self.line_bot_api.set_rich_menu_image(
                    rich_menu_id, content_type, file)
            except Exception as e:
                print("===Upload Exception===")
                raise BadRequest(e)
            return {'result': 'upload ok'}, 200
        elif usage == 'set':
            rich_menu_id = request.form['richmenu_id']
            try:
                self.line_bot_api.set_default_rich_menu(rich_menu_id)
            except:
                raise BadRequest("Maybe your richmenu id error.")
            return {'result': f'{rich_menu_id} set default ok!'}, 200
        elif usage == 'get':
            rich_menu_list = self.line_bot_api.get_rich_menu_list()
            total = []
            for rich_menu in rich_menu_list:
                total.append(rich_menu.rich_menu_id)
            return {'result': total}, 200
        elif usage == 'delete':
            rich_menu_id = request.form['richmenu_id']
            try:
                self.line_bot_api.delete_rich_menu(rich_menu_id)
            except:
                raise BadRequest("Maybe your richmenu id error.")
            return {'result': f'{rich_menu_id} is delete!'}, 200
        else:
            return {'message': 'fail'}, 400
