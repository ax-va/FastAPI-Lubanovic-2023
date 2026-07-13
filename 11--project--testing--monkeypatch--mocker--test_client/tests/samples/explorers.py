from app.models.explorers import ExplorerRequest, ExplorerResponse

hande_request = ExplorerRequest(
    name="Claude Hande",
    country="FR",
    description="Scarce during full moons",
)
weiser_request = ExplorerRequest(
    name="Noah Weiser",
    country="DE",
    description="Myopic machete man",
)
ax_va_request = ExplorerRequest(
    name="AxVa",
    country="DE",
    description="Just a good man",
)

hande_response = ExplorerResponse(
    id=1, **hande_request.model_dump()
)
weiser_response = ExplorerResponse(
    id=2, **weiser_request.model_dump()
)
ax_va_response = ExplorerResponse(
    id=3, **ax_va_request.model_dump()
)
