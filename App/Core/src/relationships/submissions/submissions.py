from sqlalchemy.orm import Mapped, relationship
from models import Answer, SubmissionStatusType, UserSubmissionLink, CardEntry

status: Mapped["SubmissionStatusType"] = relationship(
    "SubmissionStatusType", back_populates="submission", uselist=False
)

user_links: Mapped["UserSubmissionLink"] = relationship(
    "UserSubmissionLink", back_populates="submission"
)
card_entries: Mapped["CardEntry"] = relationship(
    "CardEntry", back_populates="submission"
)
answers: Mapped["Answer"] = relationship("Answer", back_populates="submission")
