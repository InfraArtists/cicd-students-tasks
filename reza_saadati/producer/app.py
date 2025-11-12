import pika
import random
import time
import logging
from config import (
    RABBITMQ_HOST,
    QUEUE_NAME,
    MIN_EVENTS,
    MAX_EVENTS,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    SEQUENTIAL_MODE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventProducer:
    def __init__(self, sequential=False):
        self.connection = None
        self.channel = None
        self.sequential = sequential
        self.current_event_rate = MIN_EVENTS
        self.connect_to_rabbitmq()

    def connect_to_rabbitmq(self):
        while True:
            try:
                credentials = pika.PlainCredentials(
                    RABBITMQ_USER,
                    RABBITMQ_PASSWORD
                )
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOST,
                        credentials=credentials,
                        heartbeat=600,
                        blocked_connection_timeout=300
                    )
                )
                self.channel = self.connection.channel()
                self.channel.queue_declare(
                    queue=QUEUE_NAME,
                    durable=True,
                    arguments={
                        'x-message-ttl': 86400000,
                        'x-max-length': 100000
                    }
                )
                logger.info("Successfully connected to RabbitMQ with authentication")
                break
            except pika.exceptions.AMQPConnectionError as e:
                logger.error(f"RabbitMQ connection failed: {str(e)}")
                logger.warning("Retrying in 5 seconds...")
                time.sleep(5)
            except pika.exceptions.ChannelError as e:
                logger.error(f"Channel error: {str(e)}")
                time.sleep(5)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                time.sleep(5)

    def get_next_event_rate(self):
        if self.sequential:
            rate = self.current_event_rate
            self.current_event_rate += 1
            if self.current_event_rate > MAX_EVENTS:
                self.current_event_rate = MIN_EVENTS
            return rate
        else:
            return random.randint(MIN_EVENTS, MAX_EVENTS)

    def produce_events(self):
        try:
            while True:
                events_per_second = self.get_next_event_rate()
                delay = 1.0 / events_per_second if events_per_second > 0 else 1.0

                for _ in range(events_per_second):
                    message = f"Event at {time.time()}"
                    self.channel.basic_publish(
                        exchange='',
                        routing_key=QUEUE_NAME,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # persistent
                        ))
                    logger.debug(f"Sent: {message}")
                    time.sleep(delay)

                logger.info(f"Produced {events_per_second} events/sec")

        except pika.exceptions.AMQPConnectionError:
            logger.error("Connection lost, reconnecting...")
            self.connect_to_rabbitmq()
            self.produce_events()

if __name__ == "__main__":
    logger.info(f"Sequential mode is {'ON' if SEQUENTIAL_MODE else 'OFF'}")
    producer = EventProducer(sequential=SEQUENTIAL_MODE)
    producer.produce_events()