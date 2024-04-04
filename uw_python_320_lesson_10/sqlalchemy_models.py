"""SQL alchemy database schema"""
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclaritiveBase, Mapped, mapped_column
# pylint: disable=R0903
class BaseModel(DeclaritiveBase):
    """Base model for SQLalchemy"""
    pass

class Users(BaseModel):
    """Users model for SQLalchemy"""
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))
    user_last_name: Mapped[str] = mapped_column(String(100))

class Statuses(BaseModel):
    """Statuses model for SQLalchemy"""
    __tablename__ = "status"

    status_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    status_text: Mapped[str] = mapped_column(String(100))

class Pictures(BaseModel):
    """Pictures model for SQLalchemy"""
    __tablename__ = "pictures"

    picture_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    tags: Mapped[str] = mapped_column(String(100))
