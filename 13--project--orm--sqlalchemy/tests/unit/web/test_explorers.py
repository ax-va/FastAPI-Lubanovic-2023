from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture
from sqlalchemy.orm.session import Session

from app.models.schemas.users import UserResponse
from app.web import explorers as web
from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from tests.samples.explorers import (
    hande_request,
    hande_response,
)


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (hande_request,hande_response),
    ]
)
def test_create(
    sample_request: ExplorerRequest,
    sample_response: ExplorerRequest,
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
    "sample_response", [hande_response]
)
def test_get_by_id_success(
    sample_response: ExplorerResponse,
    mocker: MockerFixture,
) -> None:
    db_session_mock = MagicMock(spec=Session)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = sample_response

    explorer = web.get_by_id(db_session_mock, sample_response.id)
    assert explorer == sample_response

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
        assert e.value.detail == f"Explorer with ID {sample_id} not found"

    service_mock.get_by_id.assert_called_once_with(db_session_mock, sample_id)
