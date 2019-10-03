from flask import request, redirect
from flask_restful import Resource
import requests
import os
import jwt
import json

class LineLoginController(Resource):
    def get(self):
        r = requests.post(
            "https://api.line.me/oauth2/v2.1/token",
            data={
                "grant_type": "authorization_code",
                "code": request.args.get('code'),
                "redirect_uri": os.environ.get('LINE_LOGIN_URI'),
                "client_id": os.environ.get('LINE_LOGIN_CLIENT_ID'),
                "client_secret": os.environ.get('LINE_LOGIN_SECRET'),
            }, headers={"Content-Type": "application/x-www-form-urlencoded"})
        payload = json.loads(r.text)
        print(payload)
        token = payload.get("id_token")
        if token is None:
            return {'result': payload['error_description']}, 400

        state = request.args.get('state')
        token = token.encode()
        dt = jwt.decode(token, state, None, algorithms=['HS256'])
        if dt:
            return redirect("https://line.me/R/ti/p//@127ojvgz", code=302)
            # return {'result': dt}, 200

    def post(self):
        r_uri = os.environ.get("LINE_LOGIN_URI")
        client = os.environ.get("LINE_LOGIN_CLIENT_ID")
        state = "nostate"  # it will be random value
        uri = f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={client}&redirect_uri={r_uri}&scope=profile%20openid%20email&state={state}"
        return {'result': uri}
