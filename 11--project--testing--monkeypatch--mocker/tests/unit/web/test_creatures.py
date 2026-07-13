import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture

from app.web import creatures as web
from app.models.creatures import CreatureRequest, CreatureResponse
from tests.fake.creature_samples import (
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
    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.create.return_value = sample_response

    result = web.create(sample_request)
    assert result == sample_response

    service_mock.create.assert_called_once_with(sample_request)


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, yeti_response),
    ]
)
def test_get_by_id_success(
    sample_id: int,
    sample_response: CreatureResponse,
    mocker: MockerFixture,
) -> None:
    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = sample_response

    creature = web.get_by_id(sample_id)
    assert creature == sample_response

    service_mock.get_by_id.assert_called_once_with(sample_id)


@pytest.mark.negative
@pytest.mark.parametrize(
    "sample_id", [99]
)
def test_get_by_id_not_found(
        sample_id: int,
        mocker: MockerFixture,
) -> None:
    service_mock = mocker.patch.object(web, 'service', autospec=True)
    service_mock.get_by_id.return_value = None

    with pytest.raises(HTTPException) as e:
        web.get_by_id(sample_id)
        assert e.value.status_code == 404
        assert e.value.detail == f"Creature with ID {sample_id} not found"

    service_mock.get_by_id.assert_called_once_with(sample_id)
