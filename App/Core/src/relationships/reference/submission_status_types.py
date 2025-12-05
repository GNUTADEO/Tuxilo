from sqlalchemy.orm import Mapped, relationship
from models import Submission

submission: Mapped["Submission"] = relationship(
    "Submission", back_populates="status", uselist=False
)
