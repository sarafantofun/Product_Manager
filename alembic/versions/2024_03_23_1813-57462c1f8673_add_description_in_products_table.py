"""Add description in Products Table

Revision ID: 57462c1f8673
Revises: 4ec59dc8c42d
Create Date: 2024-03-23 18:13:52.904163

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "57462c1f8673"
down_revision: Union[str, None] = "4ec59dc8c42d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "products",
        sa.Column("description", sa.Text(), server_default="", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("products", "description")
    # ### end Alembic commands ###
