from flask import request
from flask_restful import Resource, reqparse
import requests
import json
from lib.db import Database
import psycopg2.extras
import os
import boto3

cli = boto3.client("sqs", region_name=os.environ("region"))


def send_message(url, attr, body, delay=0):
    cli.send_message(
        QueueUrl=url,
        DelaySeconds=0,
        MessageAttributes=attr,
        MessageBody=body,
    )


class SendNotifyBySQSController(Resource):

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
