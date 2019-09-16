from flask_restful import Resource, reqparse
import json
from lib.db import Database
import psycopg2.extras
import os
import boto3

cli = boto3.client("sqs", region_name=os.getenv("REGION"))


def send_message(url, attr, body, delay=0):
    cli.send_message(
        QueueUrl=url,
        DelaySeconds=0,
        MessageAttributes=attr,
        MessageBody=body,
    )


class SendNotifyBySQSController(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'message', required=True, help='message can not be blank!')
        args = parser.parse_args()
        msg = args['message']
        with Database() as db, db.connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"SELECT token FROM notify")
                fetchs = cur.fetchall()
        for fetch in fetchs:
            body = {
                'token': f"{fetch['token']}",
                'message': f"Hello everyone, {msg}"
            }
            cli.send_message(
                QueueUrl=os.getenv("SQS_URL"),
                DelaySeconds=0,
                MessageAttributes={},
                MessageBody=json.dumps(body)
            )
        return {'result': 'ok'}, 200
