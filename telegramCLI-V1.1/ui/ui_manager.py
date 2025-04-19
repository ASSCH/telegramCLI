import curses
from core.app_state import State

class UIManager:
    def __init__(self, stdscr, state, contacts):
        self.stdscr = stdscr
        self.state = state
        self.contacts = contacts
        curses.curs_set(1)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.stdscr.timeout(100)

    def draw(self):
        match self.state.current_state:
            case State.MAIN_MENU:
                self._draw_main_menu()
            case State.CHAT_SELECTION:
                self._draw_chat_selection()
            case State.CHAT_VIEW:
                self._draw_chat_view()
            case State.ADD_CHAT:
                self._draw_add_chat()
            case State.DEV_INFO:
                self._draw_dev_info()

    def _draw_main_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        title = "📲 Telegram CLI"
        self.stdscr.addstr(1, (w - len(title)) // 2, title)

        menu = ["Выбрать чат", "Просмотреть историю", "Очистить историю", "Добавить чат", "О разработке", "Выход"]
        for i, item in enumerate(menu):
            x = (w - len(item)) // 2
            y = h // 2 - len(menu) // 2 + i
            if i == self.state.selected_index:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, f"> {item} <")
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, item)
        self.stdscr.refresh()

    def _draw_chat_selection(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(1, (w - len("📇 Выберите чат")) // 2, "📇 Выберите чат")

        keys = self.contacts.get_all_names()
        for i, name in enumerate(keys):
            x = (w - len(name)) // 2
            y = h // 2 - len(keys) // 2 + i
            if i == self.state.selected_index:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, f"> {name} <")
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, name)
        self.stdscr.refresh()

    def _draw_chat_view(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        title = f"💬 Чат с {self.state.active_chat}"
        self.stdscr.addstr(1, (w - len(title)) // 2, title)

        max_lines = h - 6
        start = max(0, len(self.state.messages) - max_lines)

        for i, (sender, text) in enumerate(self.state.messages[start:]):
            line = f"{sender}: {text}"
            self.stdscr.addstr(3 + i, 2, line[:w - 4])

        self.stdscr.addstr(h - 3, 2, "✏️ Введите сообщение:")
        self.stdscr.addstr(h - 2, 2, "> " + self.state.input_text[:w - 4])
        self.stdscr.addstr(h - 1, w - len("ESC: Назад | Enter: Отправить") - 2, "ESC: Назад | Enter: Отправить")
        self.stdscr.refresh()

    def _draw_add_chat(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(1, (w - len("➕ Добавить новый чат")) // 2, "➕ Добавить новый чат")

        self.stdscr.addstr(h//2 - 1, 2, "Имя чата:")
        self.stdscr.addstr(h//2, 4, self.state.new_chat_name)

        self.stdscr.addstr(h//2 + 2, 2, "Chat ID:")
        self.stdscr.addstr(h//2 + 3, 4, self.state.new_chat_id)

        self.stdscr.addstr(h - 1, w - len("ESC: Назад | Enter: Отправить") - 2, "ESC: Назад | Enter: Отправить")
        self.stdscr.refresh()

    def _draw_dev_info(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(1, (w - len("✏️ О разработке")) // 2, "✏️ О разработке")
        self.stdscr.addstr(h//2, w//2 - 20, "Данный клиент был разработан для общества.")
        self.stdscr.addstr(h//2 + 1, w//2 - 16, "Код свободен для изменений комьюнити.")
        self.stdscr.addstr(h//2 + 2, w//2 - 21, "Разработан с помощью ИИ и хакера доброй воли.")
        self.stdscr.refresh()
