"""add_role_column_user_table

Revision ID: c34a931382eb
Revises: 5790fbed67de
Create Date: 2024-11-08 22:35:57.550320

"""
from alembic import op
import sqlalchemy as sa
import enum
class UserRole(enum.Enum):
    ADMIN = 0
    NORMAL = 1


# revision identifiers, used by Alembic.
revision = 'c34a931382eb'
down_revision = '5790fbed67de'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("role", sa.Enum(UserRole), nullable = False)
    )


def downgrade():
    op.drop_column("user", "role")
