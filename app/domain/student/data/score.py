from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import AnyUrl, BaseModel
from app.shared.domain.data.entity import Entity


class CreateScoreProps(BaseModel):
    subject_name: Optional[str]
    subject_id: Optional[UUID]
    score: Optional[str]
    date: Optional[date]



class ScoreProps(CreateScoreProps, Entity):
    profile_id: UUID
    test_id: UUID

    class Config:
        allow_mutation = True
        orm_mode = True


@dataclass
class Score:
    props: ScoreProps

    @staticmethod
    def create_from(props: CreateScoreProps, profile_id: UUID, test_id: UUID) -> Score:
        score_props = ScoreProps(
            id=uuid4(),
            profile_id=profile_id,
            score=props.score,
            date=props.date,
            subject_name=props.subject_name,
            test_id= test_id,
            subject_id=props.subject_id,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return Score(props=score_props)

    def update_from(self, props: CreateScoreProps, test_id: UUID) -> Score:
        score_props = ScoreProps(
            **dict(
                self.props.dict(),
                score=props.score,
                date=props.date,
                subject_name=props.subject_name,
                subject_id=props.subject_id,
                test_id=test_id,
            )
        )
        self.props = score_props

    def delete_score(self) -> Score:
        score_props = ScoreProps(
            **dict(
                self.props.dict(),
                deleted=True,
            )
        )
        self.props = score_props
