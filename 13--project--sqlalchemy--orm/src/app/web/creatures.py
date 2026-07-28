from fastapi import APIRouter, HTTPException

from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.models.schemas.explorers import ExplorerResponse
from app.services import creatures as creatures_service
from app.services import explorer_creature as explorer_creature_service
from app.services.errors import NotFoundError, DuplicateBindingError
from app.web.deps.auth import CurrentUser
from app.web.deps.database import DatabaseSession
from app.web.errors import resource_with_id_not_found
from app.web.metadata import NOT_FOUND, UNAUTHORIZED, CONFLICT

service = creatures_service
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public API
@router.get("")
def get_all(
    db_session: DatabaseSession,
) -> list[CreatureResponse]:
    return service.get_all(db_session)


# public API
@router.get(
    "/{creature_id}",
    responses=NOT_FOUND,
)
def get_by_id(
    db_session: DatabaseSession,
    creature_id: int,
) -> CreatureResponse:
    creature_response = service.get_by_id(db_session, creature_id)

    if creature_response is None:
        raise resource_with_id_not_found(f"Creature with ID {creature_id} not found")

    return creature_response


# API for only authenticated users
@router.post(
    "",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED,
)
def create(
    db_session: DatabaseSession,
    creature_request: CreatureRequest,
    _: CurrentUser,
) -> CreatureResponse:
    return service.create(db_session, creature_request)


# API for only authenticated users
@router.put(
    "/{creature_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def replace(
    db_session: DatabaseSession,
    creature_id: int,
    creature_request: CreatureRequest,
    _: CurrentUser,
) -> CreatureResponse:
    try:
        creature = service.replace(db_session, creature_id, creature_request)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    return creature


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete(
    "/{creature_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def delete(
    db_session: DatabaseSession,
    creature_id: int,
    _: CurrentUser,
) -> None:
    try:
        service.delete(db_session, creature_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e


# public API
@router.get(
    "/{creature_id}/explorers",
    responses=NOT_FOUND,
)
def get_explorers(
    db_session: DatabaseSession,
    creature_id: int,
) -> list[ExplorerResponse]:
    return explorer_creature_service.get_explorers(db_session, creature_id)


# API for only authenticated users
@router.post(
    "/{creature_id}/explorers/{explorer_id}",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED | NOT_FOUND | CONFLICT,
)
def bind_explorer(
    db_session: DatabaseSession,
    explorer_id: int,
    creature_id: int,
    _: CurrentUser,
) -> list[ExplorerResponse]:
    try:
        explorer_creature_service.bind(
            db_session,
            explorer_id,
            creature_id,
        )

    except DuplicateBindingError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    return explorer_creature_service.get_explorers(db_session, creature_id)
