from sqlalchemy import String, Text

from sqlalchemy.orm import Mapped, mapped_column

from app.api.db.models import Base


class Product(Base):
    title: Mapped[str] = mapped_column(String(30))
    price: Mapped[float]
    count: Mapped[int]
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
