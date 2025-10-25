from logging import getLogger

# from faststream import FastStream
from faststream.rabbit import RabbitBroker

# , QueueType, RabbitExchange, RabbitQueue
from src.config import get_settings
from src.infra.broker.tasks import background_router

logger = getLogger()
broker = RabbitBroker(
    url=get_settings().RMQ_URL.unicode_string(),
    logger=logger,
)
broker.include_router(background_router)
# faststream_app = FastStream(broker, logger=logger)


# @faststream_app.after_startup
# async def declare_exchanges_and_queues() -> None:
#     dlq = await broker.declare_queue(
#         queue=RabbitQueue(
#             name="dlq",
#             queue_type=QueueType.QUORUM,
#             durable=True,
#             arguments={
#                 "x-message-ttl": 12 * 60 * 60 * 1000,
#                 "x-delivery-limit": 5,
#             },
#         ),
#     )
#     dlx = await broker.declare_exchange(
#         exchange=RabbitExchange(
#             name="dlx",
#             durable=True,
#         ),
#     )
#     await dlq.bind(exchange=dlx, routing_key=dlq.name)
