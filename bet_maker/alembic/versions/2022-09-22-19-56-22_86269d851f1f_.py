"""empty message

Revision ID: 86269d851f1f
Revises: 8a0f6a6aa582
Create Date: 2022-09-22 19:56:22.281268

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "86269d851f1f"
down_revision = "8a0f6a6aa582"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "bet",
        "id",
        existing_type=postgresql.UUID(),
        type_=postgresql.UUID(as_uuid=True),
        existing_nullable=False,
    )
    op.alter_column(
        "bet",
        "state",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=16),
        nullable=True,
    )
    op.alter_column(
        "bet",
        "deadline",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
    op.alter_column(
        "bet",
        "coefficient",
        existing_type=sa.NUMERIC(precision=14, scale=4),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "bet",
        "coefficient",
        existing_type=sa.NUMERIC(precision=14, scale=4),
        nullable=False,
    )
    op.alter_column(
        "bet",
        "deadline",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.alter_column(
        "bet",
        "state",
        existing_type=sa.String(length=16),
        type_=sa.VARCHAR(length=50),
        nullable=False,
    )
    op.alter_column(
        "bet",
        "id",
        existing_type=postgresql.UUID(as_uuid=True),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
