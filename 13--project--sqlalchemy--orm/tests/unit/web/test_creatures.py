from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture
from sqlalchemy.orm.session import Session

from app.models.schemas.users import UserResponse
from app.web import creatures as web
from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from tests.samples.creatures import (
    yeti_request,
    yeti_response,
)


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (yeti_request,yeti_response),
    ]
)
def test_create(
    sample_request: CreatureRequest,
    sample_response: CreatureResponse,
    mocker: MockerFixture,
) -> None:
    db_session_mock = MagicMock(spec=Session)
    user_response_mock = MagicMock(spec=UserResponse)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.create.return_value = sample_response

    result = web.create(db_session_mock, sample_request, user_response_mock)
    assert result == sample_response

    service_mock.create.assert_called_once_with(db_session_mock, sample_request)


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_response", [yeti_response]
)
def test_get_by_id_success(
    sample_response: CreatureResponse,
    mocker: MockerFixture,
) -> None:
    db_session_mock = MagicMock(spec=Session)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = sample_response

    creature = web.get_by_id(db_session_mock, sample_response.id)
    assert creature == sample_response

    service_mock.get_by_id.assert_called_once_with(db_session_mock, sample_response.id)


@pytest.mark.negative
@pytest.mark.parametrize(
    "sample_id", [99]
)
def test_get_by_id_not_found(
    sample_id: int,
    mocker: MockerFixture,
) -> None:
    db_session_mock = MagicMock(spec=Session)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = None

    with pytest.raises(HTTPException) as e:
        web.get_by_id(db_session_mock, sample_id)
        assert e.value.status_code == 404
        assert e.value.detail == f"Creature with ID {sample_id} not found"

    service_mock.get_by_id.assert_called_once_with(db_session_mock, sample_id)
