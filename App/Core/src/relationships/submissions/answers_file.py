from sqlalchemy.orm import Mapped, relationship
from models import Answer

answer: Mapped["Answer"] = relationship("Answer", back_populates="file_answer")
