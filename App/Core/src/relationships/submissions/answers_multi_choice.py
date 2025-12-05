from sqlalchemy.orm import Mapped, relationship
from models import Answer, MultiChoiceOptionLink

option_links: Mapped[list["MultiChoiceOptionLink"]] = relationship(
    "MultiChoiceOptionLink", back_populates="answer", cascade="all, delete-orphan"
)
answer: Mapped["Answer"] = relationship(
    "Answer", back_populates="multi_choice_answer"
)  # adjust name for each type
