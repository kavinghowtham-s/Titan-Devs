from abc import ABC, abstractmethod
from typing import Optional

class ChannelAdapter(ABC):
    @abstractmethod
    async def send_outbound(
        self,
        recipient_address: str,
        subject: Optional[str],
        body_text: str,
        reply_to_id: Optional[int] = None
    ) -> bool:
        """Dispatches an outbound message to a customer or supplier."""
        pass

