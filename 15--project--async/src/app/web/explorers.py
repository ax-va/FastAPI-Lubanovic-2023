from fastapi import APIRouter, HTTPException

from app.models.schemas.creatures import CreatureResponse
from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers as explorers_service
from app.services.errors import NotFoundError, DuplicateBindingError
from app.web.deps.auth import CurrentUser
from app.web.deps.database import DatabaseSession
from app.web.errors import resource_with_id_not_found
from app.web.metadata import NOT_FOUND, UNAUTHORIZED, CONFLICT

service = explorers_service
router = APIRouter(prefix="/explorers", tags=["Explorers"])


# public API
@router.get("")
async def get_all(
    db_session: DatabaseSession,
) -> list[ExplorerResponse]:
    return await service.get_all(db_session)


# public API
@router.get(
    "/{explorer_id}",
    responses=NOT_FOUND,
)
async def get_by_id(
    db_session: DatabaseSession,
    explorer_id: int,
) -> ExplorerResponse:
    explorer_response: ExplorerResponse | None = await service.get_by_id(db_session, explorer_id)

    if explorer_response is None:
        raise resource_with_id_not_found(f"Explorer with ID {explorer_id} not found")

    return explorer_response


# API for only authenticated users
@router.post(
    "",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED,
)
async def create(
    db_session: DatabaseSession,
    explorer: ExplorerRequest,
    _: CurrentUser,
) -> ExplorerResponse:
    return await service.create(db_session, explorer)


# API for only authenticated users
@router.put(
    "/{explorer_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
async def replace(
    db_session: DatabaseSession,
    explorer_id: int,
    explorer: ExplorerRequest,
    _: CurrentUser,
) -> ExplorerResponse:
    try:
        explorer_response: ExplorerResponse = await service.replace(db_session, explorer_id, explorer)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return explorer_response


@router.patch("/{explorer_id}")
async def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete(
    "/{explorer_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
async def delete(
    db_session: DatabaseSession,
    explorer_id: int,
    _: CurrentUser,
) -> None:
    try:
        await service.delete(db_session, explorer_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))


# API for only authenticated users
@router.post(
    "/{explorer_id}/creatures/{creature_id}",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED | NOT_FOUND | CONFLICT,
)
async def bind(
    db_session: DatabaseSession,
    explorer_id: int,
    creature_id: int,
     _: CurrentUser,
) -> list[CreatureResponse]:
    try:
        creature_responses: list[CreatureResponse] = await service.bind(
            db_session,
            explorer_id,
            creature_id,
        )

    except DuplicateBindingError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    return creature_responses


# public API
@router.get(
    "/{explorer_id}/creatures",
    responses=NOT_FOUND,
)
async def get_creatures(
    db_session: DatabaseSession,
    explorer_id: int,
) -> list[CreatureResponse]:
    return await service.get_creatures(db_session, explorer_id)
