from pydantic import Field, BaseModel
from uuid import UUID
from datetime import datetime
from app.domain.student.data.test import CreateTestProps, TestProps


class CreateTestDTO(CreateTestProps):
    pass


class UpdateTestDTO(CreateTestProps):
    pass


class TestResponseDTO(TestProps):
    pass
