from pydantic import BaseModel

class Project(BaseModel):
    id: int
    name: str
    location: str
    client: str
    budget: float
    status: str