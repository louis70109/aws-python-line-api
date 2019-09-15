# Aws-python-line-api

# Bebore you start

- LINE Notify service

- Need create a S3 Bucket

  - replace `views/notify_index.html` **YOUR_CLIENT_ID** & **YOUR_REDIRECT_URI** to your LINE notify settings
  - replace `views/notify_confirm.html` SLS_URI to your **DEPLOY domain**
  - upload both of views/ file to S3 Bucket

- Replace `controller/notify_controller.py` to your LINE notify settings
  - YOUR_REDIRECT_URI
  - YOUR_CLIENT_ID
  - YOUR_CLIENT_SECRET

# Quick Start

1. Install serverless via npm

```bash=
$ npm install -g serverless
```

2. Setup your **AWS** ceritficate

```bash=
export AWS_ACCESS_KEY_ID=<your-key-here>
export AWS_SECRET_ACCESS_KEY=<your-secret-key-here>
```

3. Clone this project

```bash=
$ serverless install --url https://github.com/louis70109/aws-python-line-notify-auth -n <YOUR_FILE_NAME>
$ cd <YOUR_FILE_NAME>/
```

4. Deploy the webhhok function

```bash=
npm install
pip install -r requirements.txt
serverless deploy
```

Now you can open `notify_index.html` url (in S3) and click button to connect LINE notify service,
Then you can get notify access_token in `notify_confirm's` page :)

If any question you can send issue for me !

# License

MIT
