from sqlalchemy.orm import Mapped, relationship
from models import Actor, ActorSegment

ActorSegment.actors = relationship("Actor", back_populates="actor_segment")
