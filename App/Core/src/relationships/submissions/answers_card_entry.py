from sqlalchemy.orm import Mapped, relationship
from models import Answer, CardTemplate, Submission

card_template: Mapped["CardTemplate"] = relationship(
    "CardTemplate", back_populates="card_entries"
)
submission: Mapped["Submission"] = relationship(
    "Submission", back_populates="card_entries"
)
answers: Mapped[list["Answer"]] = relationship(
    "Answer", back_populates="card_entry", cascade="all, delete-orphan"
)
