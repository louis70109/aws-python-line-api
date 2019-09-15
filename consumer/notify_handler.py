import json
import requests


def webhook(event, context):
    print(event)
    body = json.loads(event['Records'][0]['body'])
    print(body)
    headers = {
        'Authorization': f"Bearer {body['token']}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('https://notify-api.line.me/api/notify',
                      headers=headers,
                      data={'message': body['message']})
    print(r)

# AWS record sample
# {'Records': [{'messageId': 'fddc42ba-a122-4581-965e-d0144ac8a5ad', 'receiptHandle': 'AQEBjO32gY5pXOfOrmDR0hD4k1av9KyjbHFpc+rIBPV2Brif7Lo+jqnGevSjfFwlICyGf+BhWwKaxFw8XdB3QTzRbw0vnLURjnQeDSBrJHa/S57SRs9TOLRBq38maycAVg69iZbetg9VhLMBCcLtOtPHTzKkmo+/Sosm51WA5CzXK7A0rteikx6nxS1CUIpq6MAujodupP0Hgr5RjK5nH/nmxA4Db0leWEmLokalZbtlx4W14tp7PZxPOrQOLDaGrH//p4h32tY8IN3MkCqi+gyNT7kCU4KwCGOIrybb07ZWyKBTKw+KOMNr/Ykj4z2N1qxIvTM55UY9d8V29YsH32OjrZTei5P7Nke/51E2tWkmkqoFAlqzxDjQPvpP+Pvvr8aazeeZ6opkr59UefAiiyM71Q==', 'body': 'hi', 'attributes': {'ApproximateReceiveCount': '9', 'SentTimestamp': '1566621263072', 'SenderId': '901588721449', 'ApproximateFirstReceiveTimestamp': '1566621263072'}, 'messageAttributes': {}, 'md5OfBody': '49f68a5c8493ec2c0bf489821c21fc3b', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-east-1:901588721449:LINE_notify_consumer', 'awsRegion': 'us-east-1'}]}
