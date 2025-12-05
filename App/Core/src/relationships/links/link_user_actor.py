from sqlalchemy.orm import Mapped, relationship
from models import User, Actor, Role

user: Mapped["User"] = relationship("User", backref="actor_links")
actor: Mapped["Actor"] = relationship("Actor", back_populates="user_links")
roles: Mapped["Role"] = relationship("Role", backref="user_actor_link")
