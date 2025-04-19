from core.app_state import AppState
from core.telegram_bot import TelegramBot
from core.contact_manager import ContactManager
from core.history_manager import ChatHistoryManager
from ui.ui_manager import UIManager
from ui.input_handler import InputHandler
import curses
import threading

class TelegramCLIApp:
    def __init__(self):
        self.state = AppState()
        self.contacts = ContactManager()
        self.history = ChatHistoryManager()
        self.bot = TelegramBot(self.contacts, self.history)
        self.ui = None
        self.handler = None

    def start(self):
        threading.Thread(target=self.bot.receive_loop, args=(self.state,), daemon=True).start()
        curses.wrapper(self.run)

    def run(self, stdscr):
        self.ui = UIManager(stdscr, self.state, self.contacts)
        self.handler = InputHandler(self.state, self.bot, self.contacts, self.history)

        while True:
            self.ui.draw()
            try:
                key = stdscr.get_wch()
                self.handler.handle(key)
            except curses.error:
                continue

if __name__ == "__main__":
    TelegramCLIApp().start()
