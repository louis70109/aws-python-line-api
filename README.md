# Aws-python-line-api

## Introduction

This is a sample using `Serverless` framework to build `LINE` services in `AWS` project, if you like this, please star me :)

## Bebore you start

- LINE account
  - Notify
  - Login
  - Message api
  - LIFF
  - Love
- AWS account
  - Secret key
  - create a S3 Bucket
  - Route 53 domain
  - Love

## Quick Start

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

4. create a `.env` file and input your service key in this file

```
NOTIFY_REDIRECT_URI=
NOTIFY_CLIENT_ID=
NOTIFY_CLIENT_SECRET=
REGION=us-east-2
SQS_URL=
SQS_ARN=
PG_DB=
PG_HOST=
PG_NAME=
PG_PWD=
PG_PORT=
LINE_CHANNEL_TOKEN=
LINE_CHANNEL_SECRET_KEY=
LINE_LOGIN_CLIENT_ID=
LINE_LOGIN_SECRET=
LINE_LOGIN_URI=
```

5. change domain name
   Open `serverless.yml` and roll down, change `domainName` and `cdrtificateName` to your AWS settings(Route53 and Certificate Manager).

6. Deploy the webhook function

```bash=
npm install
pip install -r requirements.txt
serverless deploy
```

7. Move `views/` files in S3

Now you can open `notify_index.html` url (in S3) and click button to connect LINE notify service,
Then you can get notify access_token in `notify_confirm's` page :)

- LIFF settings can reference my [2019_it30-day23](https://github.com/louis70109/2019_it30/tree/master/day24)
  If any question you can send issue for me !

> This project is created by IThome 30 days challenge [repository](https://ithelp.ithome.com.tw/users/20111481/ironman/2475)'s example.

## License

MIT
