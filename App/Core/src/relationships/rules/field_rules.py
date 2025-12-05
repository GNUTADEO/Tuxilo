from sqlalchemy.orm import Mapped, relationship
from models import ValidationType, Field

rule: Mapped["ValidationType"] = relationship(
    "ValidationType",
    back_populates="field_rule",
    uselist=False
)

field: Mapped["Field"] = relationship(
    "Field",
    back_populates="field_rules"
)
