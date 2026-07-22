from sqlite3 import Connection
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture

from app.models.users import UserResponse
from app.web import explorers as web
from app.models.explorers import ExplorerRequest, ExplorerResponse
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
    connection_mock = MagicMock(spec=Connection)
    user_mock = MagicMock(spec=UserResponse)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.create.return_value = sample_response

    result = web.create(connection_mock, sample_request, user_mock)
    assert result == sample_response

    service_mock.create.assert_called_once_with(connection_mock, sample_request)


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, hande_response),
    ]
)
def test_get_by_id_success(
    sample_id: int,
    sample_response: ExplorerResponse,
    mocker: MockerFixture,
) -> None:
    connection_mock = MagicMock(spec=Connection)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = sample_response

    explorer = web.get_by_id(connection_mock, sample_id)
    assert explorer == sample_response

    service_mock.get_by_id.assert_called_once_with(connection_mock, sample_id)


@pytest.mark.negative
@pytest.mark.parametrize(
    "sample_id", [99]
)
def test_get_by_id_not_found(
        sample_id: int,
        mocker: MockerFixture,
) -> None:
    connection_mock = MagicMock(spec=Connection)

    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = None

    with pytest.raises(HTTPException) as e:
        web.get_by_id(connection_mock, sample_id)
        assert e.value.status_code == 404
        assert e.value.detail == f"Explorer with ID {sample_id} not found"

    service_mock.get_by_id.assert_called_once_with(connection_mock, sample_id)
