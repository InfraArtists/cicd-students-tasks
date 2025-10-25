import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "RIonAntHCoMe")
QUEUE_NAME = os.getenv("QUEUE_NAME", "events")
MIN_EVENTS = int(os.getenv("MIN_EVENTS_PER_SEC", "1"))
MAX_EVENTS = int(os.getenv("MAX_EVENTS_PER_SEC", "10000"))
SEQUENTIAL_MODE = os.getenv("SEQUENTIAL_MODE", "false").lower() == "true"
