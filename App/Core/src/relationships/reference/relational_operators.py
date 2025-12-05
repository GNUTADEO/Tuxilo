from sqlalchemy.orm import Mapped, relationship
from models import FieldDependency, SectionDependency

field_dependency: Mapped["FieldDependency"] = relationship(
    "FieldDependency", back_populates="operator_type", uselist=False
)

section_dependency: Mapped["SectionDependency"] = relationship(
    "SectionDependency", back_populates="operator_type", uselist=False
)