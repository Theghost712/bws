from typing import Optional


class WhatsAppLink:
    async def send_message(self, phone: str, text: str, image_path: Optional[str] = None) -> bool:
        # Just generates link - actual sending is manual
        return False
