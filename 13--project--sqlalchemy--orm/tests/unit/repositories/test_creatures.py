from sqlite3 import Connection

import pytest

from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import creatures as repository
from tests.samples.creatures import (
    yeti_response,
    bigfoot_response,
    lubanovic_request,
    lubanovic_response,
)


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (lubanovic_request, lubanovic_response),
    ]
)
def test_create(
    sample_request: CreatureRequest,
    sample_response: CreatureResponse,
    creatures_sqlite_db: Connection,
):
    missing = repository.get_by_id(sample_response.id)
    assert missing is None

    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    created_id = repository.create(sample_request)
    assert created_id == sample_response.id

    num_rows_after = len(repository.get_all())
    assert num_rows_after == num_rows_before + 1

    stored = repository.get_by_id(sample_response.id)
    assert stored == sample_response

    yeti_available = repository.get_by_id(1)
    assert yeti_available == yeti_response

    bigfoot_available = repository.get_by_id(2)
    assert bigfoot_available == bigfoot_response


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, yeti_response),
        (2, bigfoot_response),
        (3, None),
    ]
)
def test_get_by_id(
    sample_id: int,
    sample_response: CreatureResponse,
    creatures_sqlite_db: Connection,
):
    got = repository.get_by_id(sample_id)
    assert got == sample_response


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, yeti_response),
        (2, bigfoot_response),
    ]
)
def test_delete_success(
    sample_id: int,
    sample_response: CreatureResponse,
    creatures_sqlite_db: Connection,
):
    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    got = repository.get_by_id(sample_id)
    assert got == sample_response

    repository.delete(sample_id)

    num_rows_after = len(repository.get_all())
    assert num_rows_after == num_rows_before - 1

    missing = repository.get_by_id(sample_id)
    assert missing is None


@pytest.mark.parametrize(
    "sample_id", [3]
)
def test_delete_not_deleted(
        sample_id: int,
        creatures_sqlite_db: Connection,
):
    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    got = repository.get_by_id(sample_id)
    assert got is None

    with pytest.raises(RuntimeError, match="not deleted"):
        repository.delete(sample_id)

    num_rows_after = len(repository.get_all())
    assert num_rows_after == num_rows_before

    missing = repository.get_by_id(sample_id)
    assert missing is None
