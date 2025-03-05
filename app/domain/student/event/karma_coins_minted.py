from uuid import UUID

from pydantic import BaseModel


class UserKarma(BaseModel):
    tag_id: UUID
    name: str | None
    karma_posts: int
    karma_duration: int


class KarmaCoinsMintedData(BaseModel):
    id: UUID
    karma_point: int
    user_karma: list[UserKarma]
    
    class Config:
        allow_mutation: True