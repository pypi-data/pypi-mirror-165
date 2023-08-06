from typing import Any, Dict

_PLUGINS: Dict[str, Any] = {}


def register(resource_type: str, creator_fn: Any) -> None:
    """Register a new resource type."""
    _PLUGINS[resource_type] = creator_fn


def fetch_plugins() -> Dict[str, Any]:
    """Fetch plugins class"""
    return _PLUGINS


def create(arguments: Dict[str, Any]) -> Any:
    """Create a resource of a specific type, given JSON data."""
    args_copy = arguments.copy()
    resource_type = args_copy.get("type")
    try:
        creator_func = _PLUGINS[resource_type]
    except KeyError:
        raise ValueError(f"unknown resource type {resource_type!r}") from None
    credentials = None
    application_id = None
    if "credentials" in args_copy:
        credentials = args_copy.pop("credentials")
    if "application_id" in args_copy:
        application_id = args_copy.pop("application_id")
    return creator_func(
        args_copy, credentials=credentials, application_id=application_id
    )
