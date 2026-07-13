import pytest
from pytest_mock import MockerFixture

from app.models.creatures import CreatureRequest, CreatureResponse
from app.services import creatures as service
from tests.fake.creature_samples import (
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
    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.create.return_value = sample_response

    result = service.create(sample_request)
    assert result == sample_response

    repository_mock.create.assert_called_once_with(sample_request)


@pytest.mark.parametrize(
    "sample_id, expected",
    [
        (1, lubanovic_response),
        (100, None),
    ]
)
def test_get_by_id(
    sample_id: int,
    expected: CreatureResponse,
    mocker: MockerFixture,
) -> None:
    repository_mock = mocker.patch.object(service, "repository", autospec=True)
    repository_mock.get_by_id.return_value = expected

    result = service.get_by_id(sample_id)
    assert result == expected

    repository_mock.get_by_id.assert_called_once_with(sample_id)
