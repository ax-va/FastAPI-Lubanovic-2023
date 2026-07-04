from fastapi import APIRouter

from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories import fake_creatures

service = fake_creatures
router = APIRouter(prefix="/creatures")


@router.get("")
@router.get("/")
def get_all() -> list[CreatureResponse]:
    return service.get_all()


@router.get("/{creature_id}")
@router.get("/{creature_id}/")
def get_one(creature_id: int) -> CreatureResponse | None:
    return service.get_one(creature_id)


@router.post("")
@router.post("/")
def create(creature: CreatureRequest) -> CreatureResponse:
    return service.create(creature)


@router.put("/{creature_id}")
@router.put("/{creature_id}/")
def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse | None:
    return service.replace(creature_id, creature)


@router.patch("/{creature_id}")
@router.patch("/{creature_id}/")
def modify(creature_id: int) -> CreatureResponse:
    raise NotImplementedError()


@router.delete("/{creature_id}")
@router.delete("/{creature_id}/")
def delete(creature_id: int) -> bool:
    return service.delete(creature_id)
