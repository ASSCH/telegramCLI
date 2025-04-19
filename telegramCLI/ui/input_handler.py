import curses
from core.app_state import State
import pygame
from config import MUSIC

pygame.mixer.init()

class InputHandler:
    def __init__(self, state, bot, contacts, history):
        self.state = state
        self.bot = bot
        self.contacts = contacts
        self.history = history

        # Музыка при запуске
        pygame.mixer.music.load(MUSIC["start"])
        pygame.mixer.music.play()

    def handle(self, key):
        try:
            is_enter = key in (10, 13, '\n', curses.KEY_ENTER)
            is_esc = key in ('\x1b', 27)
        except:
            return

        match self.state.current_state:
            case State.MAIN_MENU:
                self._handle_main_menu(key, is_enter, is_esc)
            case State.CHAT_SELECTION:
                self._handle_chat_selection(key, is_enter, is_esc)
            case State.CHAT_VIEW:
                self._handle_chat_view(key, is_enter, is_esc)
            case State.ADD_CHAT:
                self._handle_add_chat(key, is_enter, is_esc)
            case State.DEV_INFO:
                if is_esc:
                    self.state.current_state = State.MAIN_MENU
                    self.state.selected_index = 0

    def _handle_main_menu(self, key, is_enter, is_esc):
        if key in [curses.KEY_UP, 'k']:
            self.state.selected_index = max(0, self.state.selected_index - 1)
        elif key in [curses.KEY_DOWN, 'j']:
            self.state.selected_index = min(5, self.state.selected_index + 1)
        elif is_enter:
            match self.state.selected_index:
                case 0:  # Выбрать чат
                    self.state.current_state = State.CHAT_SELECTION
                    self.state.selected_index = 0
                case 1:  # Просмотреть историю
                    self._open_history()
                case 2:  # Очистить историю
                    self._clear_history()
                case 3:  # Добавить чат
                    self.state.current_state = State.ADD_CHAT
                    self.state.new_chat_name = ""
                    self.state.new_chat_id = ""
                    self.state.add_chat_field = "name"
                case 4:  # О разработке
                    self.state.current_state = State.DEV_INFO
                case 5:  # Выход
                    pygame.mixer.music.load(MUSIC["exit"])
                    pygame.mixer.music.play()
                    import time
                    time.sleep(3)
                    exit()
        elif is_esc:
            exit()

    def _handle_chat_selection(self, key, is_enter, is_esc):
        names = self.contacts.get_all_names()
        if not names:
            self.state.current_state = State.MAIN_MENU
            return

        if key == curses.KEY_UP:
            self.state.selected_index = max(0, self.state.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.state.selected_index = min(len(names) - 1, self.state.selected_index + 1)
        elif is_enter:
            self.state.active_chat = names[self.state.selected_index]
            self.state.messages = self.history.load_history(self.state.active_chat)
            self.state.input_text = ""
            self.state.current_state = State.CHAT_VIEW
        elif is_esc:
            self.state.current_state = State.MAIN_MENU
            self.state.selected_index = 0

    def _handle_chat_view(self, key, is_enter, is_esc):
        if is_esc:
            self.state.current_state = State.MAIN_MENU
            self.state.selected_index = 0
        elif self.state.active_chat:
            if is_enter:
                text = self.state.input_text.strip()
                if text:
                    error = self.bot.send_message(self.contacts.get_chat_id(self.state.active_chat), text)
                    if error:
                        self.state.messages.append(("Ошибка", error))
                    else:
                        self.history.log_message(self.state.active_chat, "Вы", text)
                        self.state.messages.append(("Вы", text))
                    self.state.input_text = ""
            elif isinstance(key, str):
                if key == '\x7f':
                    self.state.input_text = self.state.input_text[:-1]
                elif key.isprintable():
                    self.state.input_text += key
            elif isinstance(key, int) and key in (curses.KEY_BACKSPACE, 127):
                self.state.input_text = self.state.input_text[:-1]

    def _handle_add_chat(self, key, is_enter, is_esc):
        field = self.state.add_chat_field
        if is_esc:
            self.state.current_state = State.MAIN_MENU
            self.state.selected_index = 0
        elif key == '\t':
            self.state.add_chat_field = "id" if field == "name" else "name"
        elif is_enter:
            name = self.state.new_chat_name.strip()
            chat_id = self.state.new_chat_id.strip()
            if name and chat_id.lstrip('-').isdigit():
                self.contacts.add_contact(name, int(chat_id))
                self.state.messages = [("Система", f"✅ Добавлен чат {name} ({chat_id})")]
                self.state.active_chat = name
                self.state.input_text = ""
                self.state.current_state = State.CHAT_VIEW
            else:
                self.state.messages = [("Система", "⚠️ Введите корректные данные")]
                self.state.current_state = State.CHAT_VIEW
        elif isinstance(key, str):
            if key == '\x7f':
                if field == "name":
                    self.state.new_chat_name = self.state.new_chat_name[:-1]
                else:
                    self.state.new_chat_id = self.state.new_chat_id[:-1]
            elif key.isprintable():
                if field == "name":
                    self.state.new_chat_name += key
                else:
                    self.state.new_chat_id += key

    def _open_history(self):
        if self.state.active_chat:
            self.state.messages = self.history.load_history(self.state.active_chat)
        else:
            self.state.messages = [("Система", "⚠️ Сначала выберите чат")]
        self.state.current_state = State.CHAT_VIEW

    def _clear_history(self):
        if self.state.active_chat:
            result = self.history.clear_history(self.state.active_chat)
            self.state.messages = [("Система", result)]
        else:
            self.state.messages = [("Система", "⚠️ Сначала выберите чат")]
        self.state.current_state = State.CHAT_VIEW
