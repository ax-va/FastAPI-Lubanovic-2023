from app.models.creatures import CreatureRequest, CreatureResponse

yeti_request = CreatureRequest(
    name="Yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)
bigfoot_request = CreatureRequest(
    name="Bigfoot",
    country="US",
    area="*",
    description="Yeti's Cousin Eddie",
    aka="Sasquatch"
)
lubanovic_request = CreatureRequest(
    name="Lubanovic",
    country="US",
    area="*",
    description="Author",
    aka="*"
)

yeti_response = CreatureResponse(
    id=1, **yeti_request.model_dump(),
)
bigfoot_response = CreatureResponse(
    id=2, **bigfoot_request.model_dump(),
)
lubanovic_response = CreatureResponse(
    id=3, **lubanovic_request.model_dump(),
)
