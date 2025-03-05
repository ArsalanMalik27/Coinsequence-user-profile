from pydantic import Field, BaseModel
from uuid import UUID
from datetime import datetime
from app.domain.student.data.score import CreateScoreProps, ScoreProps


class CreateScoreDTO(CreateScoreProps):
    pass


class UpdateScoreDTO(CreateScoreProps):
    id: UUID | None
    deleted: bool | None


class ScoreResponseDTO(ScoreProps):
    pass
