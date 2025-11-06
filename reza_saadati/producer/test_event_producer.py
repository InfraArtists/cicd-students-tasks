import pytest
from app import EventProducer
from config import MIN_EVENTS, MAX_EVENTS

@pytest.fixture
def producer():
    # ساخت نمونه بدون اتصال واقعی به RabbitMQ
    p = EventProducer(sequential=True)
    p.connection = None
    p.channel = None
    return p

def test_event_rate_in_sequential_mode(producer):
    rate = producer.get_next_event_rate()
    assert MIN_EVENTS <= rate <= MAX_EVENTS

def test_event_rate_in_random_mode():
    p = EventProducer(sequential=False)
    p.connection = None
    p.channel = None
    rate = p.get_next_event_rate()
    assert MIN_EVENTS <= rate <= MAX_EVENTS

def test_config_values():
    assert MIN_EVENTS < MAX_EVENTS