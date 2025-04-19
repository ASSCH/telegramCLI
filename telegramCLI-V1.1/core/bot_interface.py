from abc import ABC, abstractmethod
from core.app_state import AppState

class BotInterface(ABC):
    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> str | None:
        """Отправить сообщение. Возвращает ошибку, если она есть, иначе None."""
        pass

    @abstractmethod
    def receive_loop(self, state: AppState):
        """Постоянно получать обновления. Асинхронно или в отдельном потоке."""
        pass
