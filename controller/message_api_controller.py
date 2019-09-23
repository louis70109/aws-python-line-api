from flask import Flask, request, abort
from flask_restful import Resource
import json
import os
from lib.db import Database
import psycopg2.extras
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


class LineMessageApiWebhookController(Resource):
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_TOKEN'))
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET_KEY'))

    def get(self):
        msg = request.args.get('msg')
        with Database() as db, db.connect() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM users")
            fetch = cur.fetchall()
        for user in fetch:
            # LINE push message
            self.line_bot_api.push_message(
                user['id'], TextSendMessage(text=msg))
        return {'message': msg}, 200

    def post(self):
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        event = json.loads(body)
        print(event)
        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            print(
                "Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        token = event['events'][0]['replyToken']
        if token == "00000000000000000000000000000000":
            pass
        else:
            profile = self.line_bot_api.get_profile(
                event['events'][0]['source']['userId'])
            print(profile)
            state = f"Hello 👉 `{profile.display_name}` 👈"
            id = profile.user_id
            picture = profile.picture_url
            name = profile.display_name
            try:
                with Database() as db, db.connect() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(
                        f"INSERT INTO users(id, name, picture) VALUES ('{id}', '{name}', '{picture}')")
            except Exception as e:
                print(e)
                pass
            message = event['events'][0]['message']['text']
            if message == "上一頁" or message == "下一頁":
                try:
                    rich_menu_id = self.line_bot_api.get_rich_menu_id_of_user(
                        id)
                except:
                    # link default rich menu
                    self.line_bot_api.link_rich_menu_to_user(
                        id, "richmenu-269cc28b8e8497d76c2df062b274a2ce")
                if rich_menu_id == "richmenu-269cc28b8e8497d76c2df062b274a2ce":
                    self.line_bot_api.link_rich_menu_to_user(
                        id, "richmenu-e31be74ad7e577b4752ab70c9c2a3fba")
                else:
                    self.line_bot_api.link_rich_menu_to_user(
                        id, "richmenu-269cc28b8e8497d76c2df062b274a2ce")
            else:
                self.line_bot_api.reply_message(token, TextSendMessage(
                    text=message))
            # buttons_template_message = TemplateSendMessage(
            #     alt_text='Buttons template',
            #     template=ButtonsTemplate(
            #         thumbnail_image_url=f'{picture}.jpg',
            #         title='Menu',
            #         text='Please select',
            #         actions=[
            #             PostbackAction(
            #                 label='postback',
            #                 display_text='postback text',
            #                 data='action=buy&itemid=1'
            #             ),
            #             MessageAction(
            #                 label='message',
            #                 text='message text'
            #             ),
            #             URIAction(
            #                 label='uri',
            #                 uri='http://example.com/'
            #             )
            #         ]
            #     )
            # )
            # self.line_bot_api.reply_message(token, buttons_template_message)

            # LINE reply Location message
            # self.line_bot_api.reply_message(token, LocationSendMessage(
            #     title='my location',
            #     address='Tokyo',
            #     latitude=35.65910807942215,
            #     longitude=139.70372892916203
            # ))

            # LINE reply Image and Text message
            # self.line_bot_api.reply_message(token, [TextSendMessage(
            #     text=state), ImageSendMessage(
            #     original_content_url=profile.picture_url, preview_image_url=profile.picture_url)])
        return 'OK'
