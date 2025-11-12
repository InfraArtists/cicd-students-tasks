import pytest
from unittest.mock import patch
from app import EventProducer
from config import MIN_EVENTS, MAX_EVENTS

@patch.object(EventProducer, "connect_to_rabbitmq", lambda x: None)
def test_event_rate_in_sequential_mode():
    p = EventProducer(sequential=True)
    rate = p.get_next_event_rate()
    assert MIN_EVENTS <= rate <= MAX_EVENTS

@patch.object(EventProducer, "connect_to_rabbitmq", lambda x: None)
def test_event_rate_in_random_mode():
    p = EventProducer(sequential=False)
    rate = p.get_next_event_rate()
    assert MIN_EVENTS <= rate <= MAX_EVENTS

def test_config_values():
    assert MIN_EVENTS < MAX_EVENTS