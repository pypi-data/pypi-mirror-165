class MockExceptions:

    class ClientError(Exception): pass
    class ResourceNotFoundException(Exception): pass
    class UnauthorizedSSOTokenError(Exception): pass
    class SSOTokenLoadError(Exception): pass
