from __future__ import annotations

from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, relationship

from database.base import BaseModel


class UserModel(BaseModel):
    # history_images: list[SharedMediaModel] = relationship('SharedMediaModel', backref='user')
    history_images: list[MessageModel] = relationship('MessageModel', backref='user')


class UserPropertyMixin:
    __abstract__ = True

    user: Mapped[UserModel]

    @declared_attr
    def user_id(self) -> Mapped[int]:
        return Column(Integer, ForeignKey('users.id'), nullable=False)


class MessageModel(BaseModel, UserPropertyMixin):
    """Raw"""

    raw: Mapped[dict] = Column(JSON)
    image_id: Mapped[dict] = Column(Integer)


# class SharedMediaModel(BaseModel, UserPropertyMixin):
#     """
#     photo / video / ...
#     """
#     pass