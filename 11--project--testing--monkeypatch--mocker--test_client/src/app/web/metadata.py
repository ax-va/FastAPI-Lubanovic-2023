from app.models.errors import NotFoundResponse

NOT_FOUND_RESPONSE = {
    404: {
        "model": NotFoundResponse,
        "description": "Resource not found",
    }
}