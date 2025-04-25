from typing import List, Optional

from sqlalchemy import ForeignKey, String, CheckConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_class import Base


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)

    sub_categories: Mapped[Optional[List["SubCategory"]]] = relationship(back_populates="category", lazy="selectin")


class SubCategory(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="sub_categories", lazy="joined")


class Advertisement(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="advertisements", lazy="joined", passive_deletes=True)
    sub_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('sub_category.id', ondelete="SET NULL"))
    sub_category: Mapped[Optional["SubCategory"]] = relationship(lazy="joined", passive_deletes=True)
    location: Mapped[str] = mapped_column(String(255), index=True)
    price: Mapped[Numeric] = mapped_column(Numeric(scale=2), CheckConstraint("price >= 0"))
    # Ads have to be approved
    active: Mapped[bool] = mapped_column(default=False)
    # Mark to show that owner agrees/disagrees to negotiate price
    negotiable: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str]
    contact_email: Mapped[str]
    contact_phone: Mapped[str]
    views: Mapped[int] = mapped_column(default=0)

    images: Mapped[Optional[List["AdImage"]]] = relationship(back_populates="advertisement", lazy="selectin")


class AdImage(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    image_link: Mapped[str] = mapped_column(nullable=False)

    advertisement_id: Mapped[int] = mapped_column(ForeignKey("advertisement.id", ondelete="CASCADE"))
    advertisement: Mapped["Advertisement"] = relationship(back_populates="images", lazy="joined", passive_deletes=True)
