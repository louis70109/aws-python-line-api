from flask import request
from flask_restful import Resource, reqparse
import requests
import json
from lib.db import Database
import psycopg2.extras
import os


class NotifyController(Resource):

    def get(self):
        msg = request.args.get('msg')
        with Database() as db, db.connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"SELECT token FROM notify")
                fetch = cur.fetchall()
        for f in fetch:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f"Bearer {f['token']}"
            }
            payload = {'message': msg}

            r = requests.post(
                'https://notify-api.line.me/api/notify', data=payload, headers=headers)
        return {'result': 'ok'}, 200

    # Notify auth api
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'code', required=True, help='code can not be blank!')
        args = parser.parse_args()
        code = args['code']
        # LINE notify json data
        client = {
            'grant_type': 'authorization_code', 'code': code,
            'redirect_uri': os.getenv("NOTIFY_REDIRECT_URI"),
            'client_id': os.getenv("NOTIFY_CLIENT_ID"),
            'client_secret': os.getenv("NOTIFY_CLIENT_SECRET")
        }
        # send request to auth
        r = requests.post(
            'https://notify-bot.line.me/oauth/token', data=client)
        req = json.loads(r.text)
        if req['status'] == 200:
            token = req['access_token']
            # Here is use PostgreSQL, you can change your love db
            with Database() as db, db.connect() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(
                        f"INSERT INTO notify(token) VALUES ('{token}')")
            return {'access_token': req['access_token']}, 200
        else:
            return {'message': r.text}, 200
