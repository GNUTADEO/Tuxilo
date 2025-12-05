from sqlalchemy.orm import Mapped, relationship
from models import User, Submission, Role

user: Mapped["User"] = relationship("User", backref="submission_links")
submission: Mapped["Submission"] = relationship(
    "Submission", back_populates="user_links"
)
roles: Mapped["Role"] = relationship("Role", backref="user_submission_link")
