from sqlalchemy.orm import Mapped, relationship
from models import FieldType, FieldGroup, FieldChoice, FieldRule, Answer, FieldDependency

field_type: Mapped["FieldType"] = relationship(
    "FieldType", back_populates="field", uselist=False
)
field_group: Mapped["FieldGroup"] = relationship(
    "FieldGroup", back_populates="fields"
)
field_choices: Mapped[list["FieldChoice"]] = relationship(
    "FieldChoice", back_populates="field"
)
field_rules: Mapped[list["FieldRule"]] = relationship(
    "FieldRule", back_populates="field"
)
answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="field")
dependencies_triggered_by_others: Mapped[list["FieldDependency"]] = relationship(
    "FieldDependency",
    foreign_keys="FieldDependency.target_field_id",
    back_populates="target_field"
)
dependencies_it_triggers: Mapped[list["FieldDependency"]] = relationship(
    "FieldDependency",
    foreign_keys="FieldDependency.depends_on_field_id",
    back_populates="depends_on_field"
)
