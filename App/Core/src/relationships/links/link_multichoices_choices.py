from sqlalchemy.orm import Mapped, relationship
from models import FieldChoice, MultiChoiceAnswer

choice: Mapped["FieldChoice"] = relationship(
    "FieldChoice", back_populates="answer_links"
)
answer: Mapped["MultiChoiceAnswer"] = relationship(
    "MultiChoiceAnswer", back_populates="option_links"
)
