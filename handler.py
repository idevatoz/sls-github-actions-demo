import sys
import boto3
import logging

client = boto3.client('ssm')

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


SLACK_BOT_TOKEN = \
    client.get_parameter(Name='/SLACK_BOT_TOKEN', WithDecryption=True)['Parameter']['Value']
SLACK_SIGNING_SECRET = \
    client.get_parameter(Name='/SLACK_SIGNING_SECRET', WithDecryption=True)['Parameter']['Value']

# process_before_response must be True when running on FaaS
app = App(
    token=SLACK_BOT_TOKEN,
    process_before_response=True,
    signing_secret=SLACK_SIGNING_SECRET
)


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


@app.command("/hello-bolt-python-lambda")
def respond_to_slack_within_3_seconds(ack):
    ack("Thanks!")


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def cccommand(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
