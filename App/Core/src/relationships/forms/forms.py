from sqlalchemy.orm import Mapped, relationship
from models import Section

sections: Mapped[list["Section"]] = relationship("Section", back_populates="form")
