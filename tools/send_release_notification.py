import os
from telebot import TeleBot



def send_release_notification():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    release_type = os.getenv("GITHUB_EVENT_NAME")
    release_version = os.getenv("GITHUB_REF")
    release_text = os.getenv("RELEASE_BODY")
    release_url = os.getenv("GITHUB_SERVER_URL") + os.getenv("GITHUB_REPOSITORY") + "/releases/" + os.getenv("GITHUB_RUN_ID")

    message = f"{release_type} {release_version}\n\n{release_text}\n\n{release_url}"
    
    bot = TeleBot(bot_token)
    bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    send_release_notification()
