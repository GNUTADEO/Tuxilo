from sqlalchemy.orm import Mapped, relationship, foreign, remote, and_
from models import Question, FieldGroup, CardEntry, Criteria
from shared_models.targets import TargetTable as TargetTableBase
from models.targets import TargetTable as TargetTableApp

from shared_db import merge_enums

TargetTable = merge_enums(
    "TargetTable",
    TargetTableBase,
    TargetTableApp
)

question: Mapped["Question"] = relationship(
    "Question", back_populates="card_templates"
)
field_groups: Mapped[list["FieldGroup"]] = relationship(
    "FieldGroup", back_populates="card_template"
)
card_entries: Mapped[list["CardEntry"]] = relationship(
    "CardEntry", back_populates="card_template", cascade="all, delete-orphan"
)

criteria: Mapped[list["Criteria"]] = relationship(
    "Criteria",
    primaryjoin=lambda: and_(
        foreign(Criteria.target_id) == remote(Question.id),
        Criteria.target == TargetTable.QUESTIONS.table,
    ),
    viewonly=True,
    overlaps="criteria",
)
