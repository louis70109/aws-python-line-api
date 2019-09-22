from pathlib import Path  # python3 only
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from controller.notify_controller import NotifyController
from controller.notify_sqs_controller import SendNotifyBySQSController
from controller.message_api_controller import LineMessageApiWebhookController
from controller.richmenu_api_controller import RichmenuApiRelateController
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*", "supports_credentials": True}})
api = Api(app)

api.add_resource(NotifyController, '/notify')
api.add_resource(SendNotifyBySQSController, '/notify/sqs')
api.add_resource(LineMessageApiWebhookController, '/webhook')
api.add_resource(RichmenuApiRelateController, '/richmenu')


if __name__ == '__main__':
    app.run(debug=True)
