from sqlalchemy.orm import Mapped, relationship
from models import Question, CardTemplate, Field

question: Mapped["Question"] = relationship(
    "Question", back_populates="field_groups"
)
card_template: Mapped["CardTemplate"] = relationship(
    "CardTemplate", back_populates="field_groups"
)
fields: Mapped[list["Field"]] = relationship("Field", back_populates="field_group")
