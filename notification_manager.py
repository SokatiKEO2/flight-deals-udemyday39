import requests
from dotenv import dotenv_values

ENV = dotenv_values(".env")

class NotificationManager:
    def __init__(self):
        self.bot_id = ENV["TELEGRAM_API"]
        self.user_id = ENV["TELEGRAM_USER_ID"]
    def send_sms(self, message):
        send_text = 'https://api.telegram.org/bot' + self.bot_id + '/sendMessage?chat_id=' + self.user_id + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)
        