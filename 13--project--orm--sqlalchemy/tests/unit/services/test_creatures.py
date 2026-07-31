from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.orm.session import Session

from app.models.orm.creature import Creature
from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.services import creatures as service
from tests.samples.creatures import (
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
    mocker: MockerFixture,
) -> None:
    # Mocker replaces an object with a `Mock`.
    # Use it when you want to isolate the unit under test and verify interactions
    #  (`assert_called_once_with()`, `call_count`, `call_args`, etc.).

    db_session_mock = MagicMock(spec=Session)

    created = Creature(**sample_response.model_dump())

    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.create.return_value = created

    result = service.create(db_session_mock, sample_request)
    assert result == sample_response

    repository_mock.create.assert_called_once()

    db_session_arg, sample_arg = repository_mock.create.call_args.args
    assert db_session_arg is db_session_mock
    assert isinstance(sample_arg, Creature)
    assert sample_arg.name == sample_request.name
    assert sample_arg.country == sample_request.country
    assert sample_arg.area == sample_request.area
    assert sample_arg.description == sample_request.description
    assert sample_arg.aka == sample_request.aka

    db_session_mock.commit.assert_called_once()
    db_session_mock.rollback.assert_not_called()


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, lubanovic_response),
        (100, None),
    ]
)
def test_get_by_id(
    sample_id: int,
    sample_response: CreatureResponse | None,
    mocker: MockerFixture,
) -> None:
    db_session_mock = MagicMock(spec=Session)

    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.get_by_id.return_value = (
        Creature(**sample_response.model_dump())
        if sample_response is not None
        else None
    )

    result = service.get_by_id(db_session_mock, sample_id)
    assert result == sample_response

    repository_mock.get_by_id.assert_called_once_with(db_session_mock, sample_id)
