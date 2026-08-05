from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm.explorer import Explorer
from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers as service
from tests.samples.explorers import (
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
    mocker: MockerFixture,
) -> None:
    # Mocker replaces an object with a `Mock`.
    # Use it when you want to isolate the unit under test and verify interactions
    #  (`assert_called_once_with()`, `call_count`, `call_args`, etc.).

    db_session_mock = AsyncMock(spec=AsyncSession)

    created = Explorer(**sample_response.model_dump())

    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.create.return_value = created

    result = await service.create(db_session_mock, sample_request)
    assert result == sample_response

    repository_mock.create.assert_called_once()

    db_session_arg, sample_arg = repository_mock.create.call_args.args
    assert db_session_arg is db_session_mock
    assert isinstance(sample_arg, Explorer)
    assert sample_arg.name == sample_request.name
    assert sample_arg.country == sample_request.country
    assert sample_arg.description == sample_request.description

    db_session_mock.commit.assert_awaited_once()
    db_session_mock.rollback.assert_not_awaited()


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, ax_va_response),
        (100, None),
    ]
)
async def test_get_by_id(
    sample_id: int,
    sample_response: ExplorerResponse | None,
    mocker: MockerFixture,
) -> None:
    db_session_mock = AsyncMock(spec=AsyncSession)

    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.get_by_id.return_value = (
        Explorer(**sample_response.model_dump())
        if sample_response is not None
        else None
    )

    result = await service.get_by_id(db_session_mock, sample_id)
    assert result == sample_response

    repository_mock.get_by_id.assert_awaited_once_with(db_session_mock, sample_id)
