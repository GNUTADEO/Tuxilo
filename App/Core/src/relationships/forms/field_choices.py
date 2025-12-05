from sqlalchemy.orm import Mapped, relationship
from models import MultiChoiceOptionLink, SingleChoiceAnswer, Field

answer_links: Mapped[list["MultiChoiceOptionLink"]] = relationship(
    "MultiChoiceOptionLink", back_populates="choice"
)
answer_link: Mapped["SingleChoiceAnswer"] = relationship(
    "SingleChoiceAnswer", back_populates="choice"
)
field: Mapped["Field"] = relationship("Field", back_populates="field_choices")
