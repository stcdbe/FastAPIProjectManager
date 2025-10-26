from typing import Any


class MockRabbitMQMessageBroker:
    async def send_message(self, *_args: Any, **_kwargs: Any) -> None:
        return
