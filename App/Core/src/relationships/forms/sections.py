from sqlalchemy.orm import Mapped, relationship
from models import Section, Form, Question, Info, SectionType, SectionDependency


form: Mapped["Form"] = relationship("Form", back_populates="sections")
questions: Mapped[list["Question"]] = relationship(
    "Question", back_populates="section"
)
infos: Mapped[list["Info"]] = relationship("Info", back_populates="section")

children: Mapped[list["Section"]] = relationship(
    "Section", back_populates="parent", cascade="all, delete-orphan"
)
parent: Mapped["Section | None"] = relationship(
    "Section", back_populates="children", remote_side=lambda: Section.id
)

type: Mapped["SectionType"] = relationship("SectionType", back_populates="sections")
dependencies_triggered_by_others: Mapped[list["SectionDependency"]] = relationship(
    "SectionDependency",
    foreign_keys="SectionDependency.target_section_id",
    back_populates="target_section",
)

dependencies_it_triggers: Mapped[list["SectionDependency"]] = relationship(
    "SectionDependency",
    foreign_keys="SectionDependency.depends_on_section_id",
    back_populates="depends_on_section",
)
