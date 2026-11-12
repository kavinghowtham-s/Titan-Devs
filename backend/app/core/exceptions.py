class OpsPilotException(Exception):
    """Base exception for OpsPilot AI."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class SecurityException(OpsPilotException):
    """Raised when an untrusted input trips security or prompt-injection guardrails."""
    def __init__(self, message: str):
        super().__init__(f"Security Guardrail Triggered: {message}", status_code=403)

class SQLSandboxException(OpsPilotException):
    """Raised when an employee Text-to-SQL query violates read-only or whitelist rules."""
    def __init__(self, message: str):
        super().__init__(f"SQL Sandbox Violation: {message}", status_code=400)

class ResourceNotFoundException(OpsPilotException):
    """Raised when a requested entity does not exist."""
    def __init__(self, entity: str, identifier: any):
        super().__init__(f"{entity} with ID {identifier} not found.", status_code=404)

