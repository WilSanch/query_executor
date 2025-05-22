from pydantic import BaseModel
from typing import Optional, Dict

class QueryExecutionRequest(BaseModel):
    parameters: Optional[Dict[str, str]] = None
    blob_path: str
