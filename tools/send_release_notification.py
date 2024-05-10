import os
import sys
import requests
from telebot import TeleBot

def get_github_release_info(version):
    url = f"  https://api.github.com/repos/HamletSargsyan/_tests/releases/tags/{version}"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        return release_info
    response.raise_for_status()
    

def send_release_notification():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    release_version = os.getenv("GITHUB_REF").split("/")[-1]
    release = get_github_release_info(release_version) # type: dict
        
    message = (f"<b>{release.get('name')}</b>\n\n"
               f"<i>{release.get('body')}</i>")
    
    bot = TeleBot(bot_token, parse_mode="html")
    bot.send_message(chat_id, message)

if __name__ == "__main__":
    send_release_notification()
