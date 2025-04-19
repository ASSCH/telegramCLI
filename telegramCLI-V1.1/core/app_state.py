from enum import Enum

class State(Enum):
    MAIN_MENU = 1
    CHAT_SELECTION = 2
    CHAT_VIEW = 3
    ADD_CHAT = 4
    DEV_INFO = 5

class AppState:
    def __init__(self):
        self.current_state = State.MAIN_MENU
        self.selected_index = 0
        self.active_chat = None
        self.messages = []
        self.input_text = ""

        # Для экрана "Добавить чат"
        self.new_chat_name = ""
        self.new_chat_id = ""
        self.add_chat_field = "name"
