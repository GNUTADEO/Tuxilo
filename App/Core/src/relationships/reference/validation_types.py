from sqlalchemy.orm import Mapped, relationship
from models import FieldRule

field_rule: Mapped["FieldRule"] = relationship(
    "FieldRule", back_populates="rule", uselist=False
)
