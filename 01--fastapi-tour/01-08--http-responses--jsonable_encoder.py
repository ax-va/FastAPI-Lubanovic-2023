import json
from datetime import datetime

import pytest
from fastapi.encoders import jsonable_encoder


@pytest.fixture
def data():
    return datetime(
        year=2026,
        month=6,
        day=23,
        hour=13,
        minute=42,
        second=50,
        microsecond=123456,
    )


@pytest.mark.negative
def test_json_dump(data):
    """A `datetime` cannot be serialized by `json.dumps()`."""
    with pytest.raises(TypeError, match="not JSON serializable"):
        _ = json.dumps(data)


@pytest.mark.positive
def test_jsonable_encoder(data):
    """`jsonable_encoder` converts a `datetime` to an ISO string."""
    out: str = jsonable_encoder(data)
    assert out == "2026-06-23T13:42:50.123456"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
