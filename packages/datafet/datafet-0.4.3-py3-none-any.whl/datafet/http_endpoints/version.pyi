from pydantic import BaseModel

def get_current_version() -> None: ...

class Version(BaseModel):
    version: str

async def get_version() -> None: ...
