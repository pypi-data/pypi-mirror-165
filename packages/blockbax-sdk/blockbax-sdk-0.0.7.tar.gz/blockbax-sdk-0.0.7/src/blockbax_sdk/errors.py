class BlockbaxError(Exception):
    pass


class ValidationError(BlockbaxError):
    pass


# API Errors


class BlockbaxHTTPError(BlockbaxError):
    pass


class BlockbaxUnauthorizedError(BlockbaxHTTPError):
    pass


class BlockbaxClientError(BlockbaxHTTPError):
    pass


class BlockbaxServerError(BlockbaxHTTPError):
    pass
