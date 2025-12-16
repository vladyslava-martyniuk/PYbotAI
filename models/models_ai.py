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
