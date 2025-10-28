import pytest
from unittest.mock import patch, MagicMock
from event_producer import EventProducer

# ---------- Test 1: Connection retry ----------
@patch('event_producer.pika.BlockingConnection')
@patch('event_producer.pika.ConnectionParameters')
@patch('event_producer.pika.PlainCredentials')
def test_connect_to_rabbitmq(mock_creds, mock_params, mock_conn):
    mock_channel = MagicMock()
    mock_conn.return_value.channel.return_value = mock_channel

    producer = EventProducer(sequential=False)
    producer.connect_to_rabbitmq()

    mock_creds.assert_called_once()
    mock_conn.assert_called_once()
    mock_channel.queue_declare.assert_called_once()

# ---------- Test 2: Sequential rate ----------
def test_get_next_event_rate_sequential():
    producer = EventProducer(sequential=True)
    producer.current_event_rate = 3
    rate1 = producer.get_next_event_rate()
    rate2 = producer.get_next_event_rate()
    assert rate2 == rate1 + 1 or rate2 == producer.current_event_rate

# ---------- Test 3: Random rate ----------
def test_get_next_event_rate_random(mocker):
    mocker.patch('random.randint', return_value=10)
    producer = EventProducer(sequential=False)
    rate = producer.get_next_event_rate()
    assert rate == 10

# ---------- Test 4: Produce events sends messages ----------
@patch('event_producer.time.sleep', return_value=None)
def test_produce_events_one_cycle(mock_sleep, mocker):
    mock_channel = MagicMock()
    producer = EventProducer(sequential=False)
    producer.channel = mock_channel
    mocker.patch.object(producer, 'get_next_event_rate', return_value=2)

    # Run only one iteration
    mocker.patch('event_producer.time.time', side_effect=[1.0, 2.0, 3.0])
    mocker.patch('builtins.print')
    with patch('event_producer.EventProducer.produce_events', side_effect=KeyboardInterrupt):
        try:
            producer.produce_events()
        except KeyboardInterrupt:
            pass

    assert mock_channel.basic_publish.called
