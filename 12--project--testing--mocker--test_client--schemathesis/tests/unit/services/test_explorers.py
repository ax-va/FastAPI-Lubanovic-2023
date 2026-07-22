from sqlite3 import Connection
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from app.models.explorers import ExplorerRequest, ExplorerResponse
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
def test_create(
    sample_request: ExplorerRequest,
    sample_response: ExplorerResponse,
    mocker: MockerFixture,
) -> None:
    # Mocker replaces an object with a `Mock`.
    # Use it when you want to isolate the unit under test and verify interactions
    #  (`assert_called_once_with()`, `call_count`, `call_args`, etc.).

    connection_mock = MagicMock(spec=Connection)

    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.create.return_value = sample_response.id
    repository_mock.get_by_id.return_value = sample_response

    result = service.create(connection_mock, sample_request)
    assert result == sample_response

    repository_mock.create.assert_called_once_with(connection_mock, sample_request)
    repository_mock.get_by_id.assert_called_once_with(connection_mock, sample_response.id)

    connection_mock.commit.assert_called_once_with()
    connection_mock.rollback.assert_not_called()


@pytest.mark.parametrize(
    "sample_id, expected",
    [
        (1, ax_va_response),
        (100, None),
    ]
)
def test_get_by_id(
    sample_id: int,
    expected: ExplorerResponse | None,
    mocker: MockerFixture,
) -> None:
    connection_mock = MagicMock(spec=Connection)

    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.get_by_id.return_value = expected

    result = service.get_by_id(connection_mock, sample_id)
    assert result == expected

    repository_mock.get_by_id.assert_called_once_with(connection_mock, sample_id)
