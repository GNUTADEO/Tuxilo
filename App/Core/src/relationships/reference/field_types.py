from sqlalchemy.orm import Mapped, relationship
from models import Field

field: Mapped["Field"] = relationship(
    "Field", back_populates="field_type", uselist=False
)
