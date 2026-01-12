from pydantic import BaseModel

class ProjectCreate(BaseModel):
    type: str
    sector: str
    territory: str