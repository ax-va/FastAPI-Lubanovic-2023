import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session

from app.models.orm.explorer import Explorer
from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlalchemy import explorers as repository
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
    db_session: Session,
):
    missing = repository.get_by_id(db_session, sample_response.id)
    assert missing is None

    num_rows_before = len(repository.get_all(db_session))
    assert num_rows_before == 2

    created = repository.create(db_session, Explorer(**sample_request.model_dump()))
    assert created.id == sample_response.id
    assert created.name == sample_response.name
    assert created.country == sample_response.country
    assert created.description == sample_response.description

    num_rows_after = len(repository.get_all(db_session))
    assert num_rows_after == num_rows_before + 1

    stored = repository.get_by_id(db_session, created.id)
    assert stored == created


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
    db_session: Session,
):
    got = repository.get_by_id(db_session, sample_id)

    if got is not None and sample_response is not None:
        assert got.id == sample_response.id
        assert got.name == sample_response.name
        assert got.country == sample_response.country
        assert got.description == sample_response.description

    else:
        assert got is None


@pytest.mark.parametrize(
    "sample_response",
    [
        hande_response,
        weiser_response,
    ]
)
def test_delete_success(
    sample_response: ExplorerResponse,
    db_session: Session,
):
    num_rows_before = len(repository.get_all(db_session))
    assert num_rows_before == 2

    got = repository.get_by_id(db_session, sample_response.id)
    assert got is not None
    assert got.id == sample_response.id
    assert got.name == sample_response.name
    assert got.country == sample_response.country
    assert got.description == sample_response.description

    repository.delete(db_session, got)

    num_rows_after = len(repository.get_all(db_session))
    assert num_rows_after == num_rows_before - 1

    missing = repository.get_by_id(db_session, sample_response.id)
    assert missing is None


@pytest.mark.parametrize(
    "sample_response", [ax_va_response]
)
def test_delete_transient_object(
    sample_response: ExplorerResponse,
    db_session: Session,
):
    num_rows_before = len(repository.get_all(db_session))
    assert num_rows_before == 2

    got = repository.get_by_id(db_session, sample_response.id)
    assert got is None

    with pytest.raises(InvalidRequestError):
        repository.delete(db_session, Explorer(**sample_response.model_dump()))

    num_rows_after = len(repository.get_all(db_session))
    assert num_rows_after == num_rows_before

    missing = repository.get_by_id(db_session, sample_response.id)
    assert missing is None
