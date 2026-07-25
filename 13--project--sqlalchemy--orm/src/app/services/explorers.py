from sqlalchemy.orm.session import Session

from app.models.orm.explorer import Explorer
from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlalchemy import explorers as explorers_repository
from app.services.errors import NotFoundError

repository = explorers_repository


def to_response(explorer: Explorer) -> ExplorerResponse:
    return ExplorerResponse.model_validate(explorer, from_attributes=True)


def to_dict(explorer_request: ExplorerRequest) -> dict:
    return explorer_request.model_dump()


def get_all(db_session: Session) -> list[ExplorerResponse]:
    return [to_response(creature) for creature in repository.get_all(db_session)]


def get_by_id(
    db_session: Session,
    explorer_id: int,
) -> ExplorerResponse | None:
    explorer = repository.get_by_id(db_session, explorer_id)

    return to_response(explorer) if explorer is not None else None


def create(
    db_session: Session,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    explorer = Explorer(**to_dict(explorer_request))

    try:
        created: Explorer = repository.create(db_session, explorer)

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

    return to_response(created)


def replace(
    db_session: Session,
    explorer_id: int,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    try:
        to_update: Explorer | None = repository.get_by_id(db_session, explorer_id)
        if to_update is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        updated = repository.replace(db_session, to_update, to_dict(explorer_request))

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

    return to_response(updated)


def delete(
    db_session: Session,
    explorer_id: int,
) -> None:
    try:
        to_delete: Explorer | None = repository.get_by_id(db_session, explorer_id)
        if to_delete is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.delete(db_session, to_delete)

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()
