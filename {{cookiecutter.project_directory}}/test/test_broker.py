from app import broker


def test_broker_health_check(app):
    result = broker.health_check.delay().get()
    assert result == {"detail": "ok"}, "Broker health check failed"
