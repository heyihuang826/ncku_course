class APIError(Exception):
    """Base class for all API errors"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"{self.message}")

# 400
class BadRequest(APIError):
    """
    Cannot process the request because it is malformed or incorrect.
    """
    pass

# 401
class Unauthorized(APIError):
    """
    Required authentication information is either missing or 
    not valid for the resource.
    """
    pass

# 403
class Forbidden(APIError):
    """
    Access is denied to the requested resource. The user might 
    not have enough permission.
    """
    pass

# 404
class NotFound(APIError):
    """
    The requested resource doesn't exist.
    """
    pass

# 405
class MethodNotAllowed(APIError):
    """
    The HTTP method in the request is not allowed on the resource.
    """
    pass

# 406
class NotAcceptable(APIError):
    """
    This service doesn't support the format requested in the 
    Accept header.
    """
    pass

# 409
class Conflict(APIError):
    """
    The current state conflicts with what the request expects. 
    For example, the specified parent folder might not exist.
    """
    pass

# 410
class Gone(APIError):
    """
    The requested resource is no longer available at the server.
    """
    pass

# 411
class LengthRequired(APIError):
    """
    A Content-Length header is required on the request.
    """
    pass

# 412
class PreconditionFailed(APIError):
    """
    A precondition provided in the request (such as an if-match 
    header) does not match the resource's current state.
    """
    pass

# 413
class RequestEntityTooLarge(APIError):
    """
    The request size exceeds the maximum limit.
    """
    pass

# 415
class UnsupportedMediaType(APIError):
    """
    The content type of the request is a format that is not 
    supported by the service.
    """
    pass

# 416
class RequestedRangeNotSatisfiable(APIError):
    """
    The specified byte range is invalid or unavailable.
    """
    pass

# 422
class UnprocessableEntity(APIError):
    """
    Cannot process the request because it is semantically incorrect.
    """
    pass

# 429
class TooManyRequests(APIError):
    """
    Client application has been throttled and should not attempt to 
    repeat the request until an amount of time has elapsed.
    """
    pass

# 500
class InternalServerError(APIError):
    """
    There was an internal server error while processing the request.
    """
    pass

# 501
class NotImplemented(APIError):
    """
    The requested feature isn’t implemented.
    """
    pass

# 503
class ServiceUnavailable(APIError):
    """
    The service is temporarily unavailable. You may repeat the request
    after a delay. There may be a Retry-After header.
    """
    pass

# 507
class InsufficientStorage(APIError):
    """
    The maximum storage quota has been reached.
    """
    pass

# 509
class BandwidthLimitExceeded(APIError):
    """
    Your app has been throttled for exceeding the maximum bandwidth
    cap. Your app can retry the request again after more time has 
    elapsed.
    """
    pass