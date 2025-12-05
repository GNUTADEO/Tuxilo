from sqlalchemy.orm import Mapped, relationship
from models import (
    BooleanAnswer,
    CardEntry,
    DateAnswer,
    Field,
    FileAnswer,
    MultiChoiceAnswer,
    NumberAnswer,
    SingleChoiceAnswer,
    Submission,
    TextAnswer,
)

submission: Mapped["Submission"] = relationship("Submission", back_populates="answers")
card_entry: Mapped["CardEntry"] = relationship("CardEntry", back_populates="answers")
bool_answer: Mapped["BooleanAnswer"] = relationship(
    "BooleanAnswer", back_populates="answer", uselist=False
)
date_answer: Mapped["DateAnswer"] = relationship(
    "DateAnswer", back_populates="answer", uselist=False
)
file_answer: Mapped["FileAnswer"] = relationship(
    "FileAnswer", back_populates="answer", uselist=False
)
multi_choice_answer: Mapped["MultiChoiceAnswer"] = relationship(
    "MultiChoiceAnswer", back_populates="answer", uselist=False
)
number_answer: Mapped["NumberAnswer"] = relationship(
    "NumberAnswer", back_populates="answer", uselist=False
)
single_choice_answer: Mapped["SingleChoiceAnswer"] = relationship(
    "SingleChoiceAnswer", back_populates="answer", uselist=False
)
text_answer: Mapped["TextAnswer"] = relationship(
    "TextAnswer", back_populates="answer", uselist=False
)

field: Mapped["Field"] = relationship("Field", back_populates="answers")
