from celery import Celery
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

app = Celery('tasks', broker='pyamqp://guest@localhost//')


def gateway():
    AT_APIKEY = "{AfricasTalkingApiKey}".format(
        AfricasTalkingApiKey="67f406eb5c1eb5642a6ee5acef6120363c7c4c12a8dad2745e9caf24e6119af3")
    AT_USERNAME = "{AfricasTalkingUsername}".format(
        AfricasTalkingUsername="darklotus")
    environment = None    # change this to 1 for testing
    if environment is None:
        gateway = AfricasTalkingGateway(apiKey=AT_APIKEY, username=AT_USERNAME)
    else:
        gateway = AfricasTalkingGateway(
            apiKey=AT_APIKEY, username="sandbox", environment="sandbox")
    return gateway

@app.task(bind=True)
def send_message(self, payload):
    name = payload.get("name")
    phone_number = payload.get("phone_number")
    message = "Dear {name},\n" \
              "Join SCOSIT today at SCC 100 and get to listen to Matt, an engineer from JUMO, " \
        "talk about functional programming, plus plenty of other talks and live coding sessions lined up\n" \
        "Please come with your laptop(python installed) and be seated by 7:00PM.\n" \
        "Kind regards,\n" \
        "Pius Dan - SCOSIT".format(name=name)
    sms_gateway = gateway()
    try:
        sms_gateway.sendMessage(to_=[phone_number], message_=message)
        print("message sent")
    except AfricasTalkingGatewayException as exc:
        raise self.retry(countdown=60 * 5, exc=exc)
    
    