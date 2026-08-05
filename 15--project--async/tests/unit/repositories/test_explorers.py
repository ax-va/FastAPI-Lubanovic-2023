import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession

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
async def test_create(
    sample_request: ExplorerRequest,
    sample_response: ExplorerResponse,
    db_session: AsyncSession,
):
    missing = await repository.get_by_id(db_session, sample_response.id)
    assert missing is None

    num_rows_before = len(await repository.get_all(db_session))
    assert num_rows_before == 2

    created = await repository.create(db_session, Explorer(**sample_request.model_dump()))
    assert isinstance(created, Explorer)
    assert created.id == sample_response.id
    assert created.name == sample_response.name
    assert created.country == sample_response.country
    assert created.description == sample_response.description

    num_rows_after = len(await repository.get_all(db_session))
    assert num_rows_after == num_rows_before + 1

    stored = await repository.get_by_id(db_session, created.id)
    assert stored == created


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, hande_response),
        (2, weiser_response),
        (3, None),
    ]
)
async def test_get_by_id(
    sample_id: int,
    sample_response: ExplorerResponse,
    db_session: AsyncSession,
):
    got = await repository.get_by_id(db_session, sample_id)

    if sample_response is not None:
        assert got is not None
        assert isinstance(got, Explorer)
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
async def test_delete_success(
    sample_response: ExplorerResponse,
    db_session: AsyncSession,
):
    num_rows_before = len(await repository.get_all(db_session))
    assert num_rows_before == 2

    got = await repository.get_by_id(db_session, sample_response.id)
    assert got is not None

    await repository.delete(db_session, got)

    num_rows_after = len(await repository.get_all(db_session))
    assert num_rows_after == num_rows_before - 1

    missing = await repository.get_by_id(db_session, sample_response.id)
    assert missing is None


@pytest.mark.parametrize(
    "sample_response", [ax_va_response]
)
async def test_delete_transient_object(
    sample_response: ExplorerResponse,
    db_session: AsyncSession,
):
    num_rows_before = len(await repository.get_all(db_session))
    assert num_rows_before == 2

    got = await repository.get_by_id(db_session, sample_response.id)
    assert got is None

    with pytest.raises(InvalidRequestError):
        await repository.delete(db_session, Explorer(**sample_response.model_dump()))

    num_rows_after = len(await repository.get_all(db_session))
    assert num_rows_after == num_rows_before

    missing = await repository.get_by_id(db_session, sample_response.id)
    assert missing is None
