from sqlalchemy.orm import Mapped, relationship
from models import RelationalOperator, Section

operator_type: Mapped["RelationalOperator"] = relationship(
    "RelationalOperator", back_populates="section_dependency", uselist=False
)
target_section: Mapped["Section"] = relationship(
    "Section",
    foreign_keys=[target_section_id],
    back_populates="dependencies_triggered_by_others",
)

depends_on_section: Mapped["Section"] = relationship(
    "Section",
    foreign_keys=[depends_on_section_id],
    back_populates="dependencies_it_triggers",
)
