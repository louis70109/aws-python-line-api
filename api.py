from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from controller.notify_controller import NotifyController

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*", "supports_credentials": True}})
api = Api(app)

api.add_resource(NotifyController, '/notify')

if __name__ == '__main__':
    app.run(debug=True)
