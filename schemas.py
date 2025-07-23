from pydantic import BaseModel,ConfigDict,BeforeValidator,Field
from typing import Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    full_name: str
    username: str

class UserCreate(UserBase):
    
    embeddings: list|Optional[list] = []
    is_admin: bool = False

class UserInDB(UserBase):
    hashed_embeddings:bytes
    is_admin: bool = False

class UserPublic(UserBase):
    is_admin: bool = False
    id: PyObjectId = Field(alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )



class UserToken(BaseModel):
    username: str | None = None 