from zappa.asynchronous import task
def handler(event, context):
    print(f"这是定时任务, event {event}, context: {context}")


