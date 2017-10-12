from africastalking.AfricasTalkingGateway import AfricasTalkingGatewayException
from celery import Celery

from utils import gateway

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task(bind=True)
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
    
    