from typing import Any, Dict, Optional, TypedDict


class JsonLDDocument(TypedDict):
    """Loaded document."""

    document: Dict[str, Any]
    contextUrl: Optional[str]
    documentUrl: str
    contentType: str
