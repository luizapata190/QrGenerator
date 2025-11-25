import logging
import json
from app.core.logging_config import JsonFormatter

def test_json_formatter():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None
    )
    # Simular campo extra agregado al record
    record.extra_field = "extra_value"
    
    formatted = formatter.format(record)
    log_dict = json.loads(formatted)
    
    assert log_dict["message"] == "Test message"
    assert log_dict["level"] == "INFO"
    assert log_dict["extra_field"] == "extra_value"
    assert "timestamp" in log_dict
