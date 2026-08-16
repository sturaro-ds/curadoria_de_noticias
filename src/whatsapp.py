import os
import requests
from dotenv import load_dotenv
load_dotenv()

# CHAVES
CALLMEBOT_PHONE = os.getenv('CALLMEBOT_PHONE')
CALLMEBOT_APIKEY = os.getenv('CALLMEBOT_APIKEY')

# FUNÇAO
def whatsapp_msg(resumo: dict):
    """Envia uma mensagem para o WhatsApp do próprio usuário via CallMeBot."""

    corpo = ()

    resp = requests.get(
        "https://api.callmebot.com/whatsapp.php",
        params={"phone": CALLMEBOT_PHONE, 
                "text": corpo,
                "apikey": CALLMEBOT_APIKEY},
        timeout=10,
    )
    return resp.text
