from sqlalchemy.orm import Mapped, relationship
from models import ActorSegment, UserActorLink

actor_segment: Mapped["ActorSegment"] = relationship("ActorSegment", back_populates="actors")

user_links: Mapped["UserActorLink"] = relationship(
    "UserActorLink", back_populates="actor"
)
