from sqlalchemy.orm import Mapped, relationship
from models import Section

section: Mapped["Section"] = relationship("Section", back_populates="infos")
