from abc import ABC, abstractmethod
from typing import Optional


class Sender(ABC):
    @abstractmethod
    async def send_message(self, chat_id: str, text: str, image_path: Optional[str] = None) -> bool:
        pass
