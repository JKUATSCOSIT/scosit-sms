from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from config import Config

def gateway():
    AT_APIKEY = Config.API_KEY
    AT_USERNAME = Config.USERNAME
    environment = Config.ENVIRONMENT
    if environment is None:
        gateway = AfricasTalkingGateway(apiKey=AT_APIKEY, username=AT_USERNAME)
    else:
        gateway = AfricasTalkingGateway(
            apiKey=AT_APIKEY, username="sandbox", environment="sandbox")
    return gateway
