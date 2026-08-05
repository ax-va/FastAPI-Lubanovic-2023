import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm.creature import Creature
from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlalchemy import creatures as repository
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
async def test_create(
    sample_request: CreatureRequest,
    sample_response: CreatureResponse,
    db_session: AsyncSession,
):
    missing = await repository.get_by_id(db_session, sample_response.id)
    assert missing is None

    num_rows_before = len(await repository.get_all(db_session))
    assert num_rows_before == 2

    created = await repository.create(db_session, Creature(**sample_request.model_dump()))
    assert isinstance(created, Creature)
    assert created.id == sample_response.id
    assert created.name == sample_response.name
    assert created.country == sample_response.country
    assert created.area == sample_response.area
    assert created.description == sample_response.description
    assert created.aka == sample_response.aka

    num_rows_after = len(await repository.get_all(db_session))
    assert num_rows_after == num_rows_before + 1

    stored = await repository.get_by_id(db_session, created.id)
    assert stored == created


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, yeti_response),
        (2, bigfoot_response),
        (3, None),
    ]
)
async def test_get_by_id(
    sample_id: int,
    sample_response: CreatureResponse | None,
    db_session: AsyncSession,
):
    got = await repository.get_by_id(db_session, sample_id)

    if sample_response is not None:
        assert got is not None
        assert isinstance(got, Creature)
        assert got.id == sample_response.id
        assert got.name == sample_response.name
        assert got.country == sample_response.country
        assert got.area == sample_response.area
        assert got.description == sample_response.description
        assert got.aka == sample_response.aka

    else:
        assert got is None


@pytest.mark.parametrize(
    "sample_response",
    [
        yeti_response,
        bigfoot_response,
    ]
)
async def test_delete_success(
    sample_response: CreatureResponse,
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
    "sample_response", [lubanovic_response]
)
async def test_delete_transient_object(
    sample_response: CreatureResponse,
    db_session: AsyncSession,
):
    num_rows_before = len(await repository.get_all(db_session))
    assert num_rows_before == 2

    got = await repository.get_by_id(db_session, sample_response.id)
    assert got is None

    with pytest.raises(InvalidRequestError):
        await repository.delete(db_session, Creature(**sample_response.model_dump()))

    num_rows_after = len(await repository.get_all(db_session))
    assert num_rows_after == num_rows_before

    missing = await repository.get_by_id(db_session, sample_response.id)
    assert missing is None
