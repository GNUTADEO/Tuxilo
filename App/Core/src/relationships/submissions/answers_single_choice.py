from sqlalchemy.orm import Mapped, relationship
from models import Answer, FieldChoice

choice: Mapped["FieldChoice"] = relationship(
    "FieldChoice", back_populates="answer_link"
)
answer: Mapped["Answer"] = relationship(
    "Answer", back_populates="single_choice_answer"
)  # adjust name for each type
