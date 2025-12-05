from sqlalchemy.orm import Mapped, relationship
from models import RelationalOperator, Field

operator_type: Mapped["RelationalOperator"] = relationship(
    "RelationalOperator", back_populates="field_dependency", uselist=False
)
target_field: Mapped["Field"] = relationship(
    "Field",
    foreign_keys=[target_field_id],
    back_populates="dependencies_triggered_by_others",
)
depends_on_field: Mapped["Field"] = relationship(
    "Field",
    foreign_keys=[depends_on_field_id],
    back_populates="dependencies_it_triggers",
)
