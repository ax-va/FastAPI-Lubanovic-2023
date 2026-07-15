from app.models.errors import NotFoundResponse, UnauthorizedResponse, BadRequestResponse

BAD_REQUEST = {
    400: {
        "model": BadRequestResponse,
        "description": "Invalid query parameters",
    }
}


UNAUTHORIZED = {
    401: {
        "model": UnauthorizedResponse,
        "description": "Invalid credentials",
    }
}

NOT_FOUND = {
    404: {
        "model": NotFoundResponse,
        "description": "Resource not found",
    }
}
