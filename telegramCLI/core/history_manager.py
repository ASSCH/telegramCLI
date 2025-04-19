import os
from datetime import datetime
from config import HISTORY_DIR

class ChatHistoryManager:
    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    def _get_file_path(self, chat_name: str) -> str:
        return os.path.join(HISTORY_DIR, f"{chat_name}.txt")

    def log_message(self, chat_name: str, sender: str, text: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._get_file_path(chat_name), "a", encoding="utf-8") as f:
            f.write(f"[{now}] {sender}: {text}\n")

    def load_history(self, chat_name: str) -> list[tuple[str, str]]:
        path = self._get_file_path(chat_name)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return [
                (line.split("] ")[1].split(": ")[0], ": ".join(line.split("] ")[1].split(": ")[1:]))
                for line in f.read().splitlines()
            ]

    def clear_history(self, chat_name: str) -> str:
        path = self._get_file_path(chat_name)
        if os.path.exists(path):
            os.remove(path)
            return f"🗑 История с {chat_name} очищена."
        return f"⛔ История с {chat_name} не найдена."
