from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Date
)
from sqlalchemy.orm import relationship
from base import Base


# =======================
# ROLES
# =======================
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(140), nullable=False)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r})"


# =======================
# USERS
# =======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(140), nullable=False)
    email = Column(String(254), nullable=False)
    password = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    session = Column(String(255))
    is_banned = Column(Boolean, default=False)

    role = relationship("Role", back_populates="users")
    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"


# =======================
# AI APIS
# =======================
class AiApi(Base):
    __tablename__ = "ai_api"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    url = Column(String(255), nullable=False)

    ai_api_models = relationship(
        "AiApiModel",
        back_populates="ai_api",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"AiApi(id={self.id!r}, name={self.name!r}, url={self.url!r})"


# =======================
# AI API MODELS
# =======================
class AiApiModel(Base):
    __tablename__ = "ai_api_models"

    id = Column(Integer, primary_key=True, index=True)
    ai_api_id = Column(Integer, ForeignKey("ai_api.id"), nullable=False)
    name = Column(String(50), nullable=False)

    ai_api = relationship("AiApi", back_populates="ai_api_models")
    reviews = relationship("Review", back_populates="ai_api_model")

    def __repr__(self):
        return (
            f"AiApiModel(id={self.id!r}, "
            f"ai_api_id={self.ai_api_id!r}, "
            f"name={self.name!r})"
        )


# =======================
# REVIEWS
# =======================
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ai_api_model_id = Column(Integer, ForeignKey("ai_api_models.id"), nullable=False)

    date = Column(Date, nullable=False)
    score = Column(Integer, nullable=False)

    user = relationship("User", back_populates="reviews")
    ai_api_model = relationship("AiApiModel", back_populates="reviews")

    def __repr__(self):
        return (
            f"Review(id={self.id!r}, user_id={self.user_id!r}, "
            f"ai_api_model_id={self.ai_api_model_id!r}, "
            f"date={self.date!r}, score={self.score!r})"
        )
