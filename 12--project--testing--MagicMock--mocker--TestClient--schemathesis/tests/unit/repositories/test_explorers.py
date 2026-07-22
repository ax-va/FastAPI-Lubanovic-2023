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
    db_connection: Connection,
):
    missing = repository.get_by_id(db_connection, sample_response.id)
    assert missing is None

    num_rows_before = len(repository.get_all(db_connection))
    assert num_rows_before == 2

    created_id = repository.create(db_connection, sample_request)
    assert created_id == sample_response.id

    num_rows_after = len(repository.get_all(db_connection))
    assert num_rows_after == num_rows_before + 1

    stored = repository.get_by_id(db_connection, sample_response.id)
    assert stored == sample_response

    hande_available = repository.get_by_id(db_connection, 1)
    assert hande_available == hande_response

    weiser_available = repository.get_by_id(db_connection, 2)
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
    db_connection: Connection,
):
    got = repository.get_by_id(db_connection, sample_id)
    assert got == sample_response


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, hande_response),
        (2, weiser_response),
    ]
)
def test_delete_success(
    sample_id: int,
    sample_response: ExplorerResponse,
    db_connection: Connection,
):
    num_rows_before = len(repository.get_all(db_connection))
    assert num_rows_before == 2

    got = repository.get_by_id(db_connection, sample_id)
    assert got == sample_response

    repository.delete(db_connection, sample_id)

    num_rows_after = len(repository.get_all(db_connection))
    assert num_rows_after == num_rows_before - 1

    missing = repository.get_by_id(db_connection, sample_id)
    assert missing is None


@pytest.mark.parametrize(
    "sample_id", [None]
)
def test_delete_not_deleted(
    sample_id: int,
    db_connection: Connection,
):
    num_rows_before = len(repository.get_all(db_connection))
    assert num_rows_before == 2

    got = repository.get_by_id(db_connection, sample_id)
    assert got is None

    with pytest.raises(RuntimeError, match="not deleted"):
        repository.delete(db_connection, sample_id)

    num_rows_after = len(repository.get_all(db_connection))
    assert num_rows_after == num_rows_before

    missing = repository.get_by_id(db_connection, sample_id)
    assert missing is None
