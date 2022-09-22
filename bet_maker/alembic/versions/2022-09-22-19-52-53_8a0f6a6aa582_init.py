"""init

Revision ID: 8a0f6a6aa582
Revises: 
Create Date: 2022-09-22 19:52:53.718435

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "8a0f6a6aa582"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bet",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("state", sa.String(50), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("coefficient", sa.Numeric(precision=14, scale=4), nullable=False),
    )


def downgrade():
    op.drop_table("bet")
