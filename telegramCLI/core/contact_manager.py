import json
import os
from config import CONTACTS_FILE

class ContactManager:
    def __init__(self):
        self.contacts = self.load_contacts()
        self.chat_names = {v: k for k, v in self.contacts.items()}

    def load_contacts(self):
        if not os.path.exists(CONTACTS_FILE):
            return {}
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_contacts(self):
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)

    def add_contact(self, name: str, chat_id: int):
        self.contacts[name] = chat_id
        self.chat_names[chat_id] = name
        self.save_contacts()

    def get_name(self, chat_id: int) -> str | None:
        return self.chat_names.get(chat_id)

    def get_chat_id(self, name: str) -> int | None:
        return self.contacts.get(name)

    def get_all_names(self):
        return list(self.contacts.keys())
