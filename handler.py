def echo(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

