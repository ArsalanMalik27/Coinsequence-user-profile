from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel
from app.domain.student.data.score import ScoreProps
from app.shared.domain.data.entity import Entity


class CreateTestProps(BaseModel):
    test_name: str
    test_id: Optional[UUID]


class TestProps(CreateTestProps, Entity):
    profile_id: UUID
    scores: list[ScoreProps] | None

    class Config:
        allow_mutation = True
        orm_mode = True


@dataclass
class Test:
    props: TestProps

    @staticmethod
    def create_from(props: CreateTestProps, profile_id: UUID) -> Test:
        test_props = TestProps(
            id=uuid4(),
            profile_id=profile_id,
            test_name=props.test_name,
            test_id=props.test_id,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Test(props=test_props)

    def update_from(self, props: CreateTestProps) -> Test:
        test_props = TestProps(
            **dict(
                self.props.dict(),
                test_name=props.test_name,
                test_id=props.test_id,
            )
        )
        self.props = test_props
