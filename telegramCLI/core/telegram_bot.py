import time
import requests
from config import BOT_TOKEN
from core.bot_interface import BotInterface
from core.app_state import AppState

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

class TelegramBot(BotInterface):
    def __init__(self, contact_manager, history_manager):
        self.contact_manager = contact_manager
        self.history_manager = history_manager
        self.last_update_id = None

    def send_message(self, chat_id: int, text: str) -> str | None:
        try:
            response = requests.post(f"{API_URL}/sendMessage", data={'chat_id': chat_id, 'text': text})
            if response.status_code != 200:
                return f"⚠️ Ошибка отправки: {response.text}"
        except Exception as e:
            return f"⚠️ Ошибка: {e}"
        return None

    def receive_loop(self, state: AppState):
        while True:
            updates = self._get_updates(offset=self.last_update_id)
            for update in updates.get("result", []):
                self.last_update_id = update["update_id"] + 1
                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                sender = self._get_sender_name(message)
                chat_name = self.contact_manager.get_name(chat_id)

                if chat_name:
                    self.history_manager.log_message(chat_name, sender, text)
                    if chat_name == state.active_chat:
                        state.messages.append((sender, text))

            time.sleep(1)

    def _get_updates(self, offset=None):
        try:
            response = requests.get(f"{API_URL}/getUpdates", params={'timeout': 10, 'offset': offset})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠️ Ошибка обновления: {e}")
            return {}

    def _get_sender_name(self, message):
        sender = message["from"].get("first_name", "Неизвестный")
        if "last_name" in message["from"]:
            sender += " " + message["from"]["last_name"]
        return sender
