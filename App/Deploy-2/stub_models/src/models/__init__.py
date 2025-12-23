# Minimal models - Basic implementation to make application run
from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

# Core Actor models
class ActorSegment(Base):
    __tablename__ = "actor_segments"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actors: Mapped[list["Actor"]] = relationship("Actor", back_populates="actor_segment")

class Actor(Base):
    __tablename__ = "actors"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    segment_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("actor_segments.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actor_segment: Mapped[Optional["ActorSegment"]] = relationship("ActorSegment", back_populates="actors")
    user_links: Mapped[list["UserActorLink"]] = relationship("UserActorLink", back_populates="actor")

# Auth models
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(100))
    role_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actor_links: Mapped[list["UserActorLink"]] = relationship("UserActorLink", back_populates="user")
    submission_links: Mapped[list["UserSubmissionLink"]] = relationship("UserSubmissionLink", back_populates="user")

class UserActorLink(Base):
    __tablename__ = "user_actor_links"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    actor_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("actors.id"))
    user: Mapped["User"] = relationship("User", back_populates="actor_links")
    actor: Mapped["Actor"] = relationship("Actor", back_populates="user_links")

# Form models
class SectionType(Base):
    __tablename__ = "section_types"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))

class Form(Base):
    __tablename__ = "forms"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sections: Mapped[list["Section"]] = relationship("Section", back_populates="form")

class Section(Base):
    __tablename__ = "sections"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    form_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("forms.id"))
    section_type_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("section_types.id"), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    form: Mapped["Form"] = relationship("Form", back_populates="sections")
    field_groups: Mapped[list["FieldGroup"]] = relationship("FieldGroup", back_populates="section")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="section")

class SectionDependency(Base):
    __tablename__ = "section_dependencies"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    section_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id"))
    depends_on_section_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id"))

class Info(Base):
    __tablename__ = "infos"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class FieldType(Base):
    __tablename__ = "field_types"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))

class ValidationType(Base):
    __tablename__ = "validation_types"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))

class RelationalOperator(Base):
    __tablename__ = "relational_operators"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    symbol: Mapped[str] = mapped_column(String(10))

class FieldGroup(Base):
    __tablename__ = "field_groups"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    section_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id"))
    order: Mapped[int] = mapped_column(Integer, default=0)
    section: Mapped["Section"] = relationship("Section", back_populates="field_groups")
    fields: Mapped[list["Field"]] = relationship("Field", back_populates="field_group")

class Field(Base):
    __tablename__ = "fields"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    label: Mapped[str] = mapped_column(String(255))
    field_type_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("field_types.id"))
    field_group_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("field_groups.id"))
    required: Mapped[bool] = mapped_column(Boolean, default=False)
    order: Mapped[int] = mapped_column(Integer, default=0)
    field_group: Mapped["FieldGroup"] = relationship("FieldGroup", back_populates="fields")
    choices: Mapped[list["FieldChoice"]] = relationship("FieldChoice", back_populates="field")
    rules: Mapped[list["FieldRule"]] = relationship("FieldRule", back_populates="field")

class FieldChoice(Base):
    __tablename__ = "field_choices"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    field_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fields.id"))
    label: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(String(255))
    order: Mapped[int] = mapped_column(Integer, default=0)
    field: Mapped["Field"] = relationship("Field", back_populates="choices")

class FieldRule(Base):
    __tablename__ = "field_rules"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    field_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fields.id"))
    validation_type_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("validation_types.id"), nullable=True)
    rule_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    field: Mapped["Field"] = relationship("Field", back_populates="rules")

class FieldDependency(Base):
    __tablename__ = "field_dependencies"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    field_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fields.id"))
    depends_on_field_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fields.id"))
    operator_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("relational_operators.id"), nullable=True)

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column(Text)
    section_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id"))
    order: Mapped[int] = mapped_column(Integer, default=0)
    section: Mapped["Section"] = relationship("Section", back_populates="questions")

class CardTemplate(Base):
    __tablename__ = "card_templates"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class CardEntry(Base):
    __tablename__ = "card_entries"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    card_template_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("card_templates.id"))
    submission_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("submissions.id"))

class Criteria(Base):
    __tablename__ = "criteria"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0)

# Submission models
class SubmissionStatusType(Base):
    __tablename__ = "submission_status_types"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))

class Submission(Base):
    __tablename__ = "submissions"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    form_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("forms.id"))
    actor_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("actors.id"), nullable=True)
    status_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("submission_status_types.id"), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="submission")
    user_links: Mapped[list["UserSubmissionLink"]] = relationship("UserSubmissionLink", back_populates="submission")

class UserSubmissionLink(Base):
    __tablename__ = "user_submission_links"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    submission_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("submissions.id"))
    user: Mapped["User"] = relationship("User", back_populates="submission_links")
    submission: Mapped["Submission"] = relationship("Submission", back_populates="user_links")

class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    submission_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("submissions.id"))
    field_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fields.id"))
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submission: Mapped["Submission"] = relationship("Submission", back_populates="answers")

class MultiChoiceAnswer(Base):
    __tablename__ = "multi_choice_answers"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    answer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("answers.id"))
    choice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("field_choices.id"))

class SingleChoiceAnswer(Base):
    __tablename__ = "single_choice_answers"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    answer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("answers.id"))
    choice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("field_choices.id"))

class MultiChoiceOptionLink(Base):
    __tablename__ = "multi_choice_option_links"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    answer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("answers.id"))
    choice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("field_choices.id"))

# Result models
class Result(Base):
    __tablename__ = "results"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    submission_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("submissions.id"))
    actor_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("actors.id"), nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

__all__ = [
    "Base",
    "Actor",
    "ActorSegment",
    "User",
    "Role",
    "UserActorLink",
    "Form",
    "Section",
    "SectionType",
    "SectionDependency",
    "Question",
    "Info",
    "Field",
    "FieldType",
    "FieldGroup",
    "FieldChoice",
    "FieldRule",
    "FieldDependency",
    "ValidationType",
    "RelationalOperator",
    "Answer",
    "MultiChoiceAnswer",
    "SingleChoiceAnswer",
    "MultiChoiceOptionLink",
    "Submission",
    "SubmissionStatusType",
    "UserSubmissionLink",
    "CardTemplate",
    "CardEntry",
    "Criteria",
    "Result",
]
