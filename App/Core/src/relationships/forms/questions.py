from sqlalchemy.orm import Mapped, relationship, foreign, and_
from models import Section, FieldGroup, CardTemplate, Criteria, Question
from shared_models.targets import TargetTable as TargetTableBase
from models.targets import TargetTable as TargetTableApp

from shared_db import merge_enums

TargetTable = merge_enums(
    "TargetTable",
    TargetTableBase,
    TargetTableApp
)

section: Mapped["Section"] = relationship("Section", back_populates="questions")
field_groups: Mapped[list["FieldGroup"]] = relationship(
    "FieldGroup", back_populates="question"
)
card_templates: Mapped[list["CardTemplate"]] = relationship(
    "CardTemplate", back_populates="question"
)

criteria: Mapped[list["Criteria"]] = relationship(
    "Criteria",
    primaryjoin=lambda: and_(
        foreign(Criteria.target_id) == Question.id,
        Criteria.target == TargetTable.QUESTIONS.table,
    ),
    viewonly=True,
    overlaps="criteria",
)
