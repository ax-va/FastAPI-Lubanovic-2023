from sqlite3 import Connection

import pytest

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlite import explorers as repository
from tests.samples.explorers import (
    hande_response,
    weiser_response,
    ax_va_request,
    ax_va_response,
)


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (ax_va_request, ax_va_response),
    ]
)
def test_create(
    sample_request: ExplorerRequest,
    sample_response: ExplorerResponse,
    explorers_sqlite_db: Connection,
):
    missing = repository.get_by_id(sample_response.id)
    assert missing is None

    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    created = repository.create(sample_request)
    assert created == sample_response

    num_rows_after = len(repository.get_all())
    assert num_rows_after == num_rows_before + 1

    stored = repository.get_by_id(sample_response.id)
    assert stored == sample_response

    hande_available = repository.get_by_id(1)
    assert hande_available == hande_response

    weiser_available = repository.get_by_id(2)
    assert weiser_available == weiser_response


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, hande_response),
        (2, weiser_response),
        (3, None),
    ]
)
def test_get_by_id(
    sample_id: int,
    sample_response: ExplorerResponse,
    explorers_sqlite_db: Connection,
):
    got = repository.get_by_id(sample_id)
    assert got == sample_response


@pytest.mark.parametrize(
    "sample_id, expected",
    [
        (1, True),
        (2, True),
        (3, False),

    ]
)
def test_delete(
    sample_id: int,
    expected: bool,
    explorers_sqlite_db: Connection,
):
    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    deleted = repository.delete(sample_id)
    assert deleted is expected

    num_rows_after = len(repository.get_all())
    if expected:
        assert num_rows_after == num_rows_before - 1
    else:
        assert num_rows_after == num_rows_before

    missing = repository.get_by_id(sample_id)
    assert missing is None
