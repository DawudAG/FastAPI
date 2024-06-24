"""add content column to posts table

Revision ID: 3c686b9846c0
Revises: c6566a2120cb
Create Date: 2024-06-24 21:37:56.898572

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c686b9846c0"
down_revision: Union[str, None] = "c6566a2120cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
