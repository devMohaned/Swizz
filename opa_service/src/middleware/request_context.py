from contextvars import ContextVar

# Context variable to hold the current request ID per async task
request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)

def set_request_id(request_id: str):
    request_id_ctx_var.set(request_id)

def get_request_id() -> str | None:
    return request_id_ctx_var.get()