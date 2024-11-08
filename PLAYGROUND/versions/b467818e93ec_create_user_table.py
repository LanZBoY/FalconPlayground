"""create-user-table

Revision ID: b467818e93ec
Revises: 
Create Date: 2024-11-08 12:29:09.203367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b467818e93ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('username', sa.String, nullable = False),
        sa.Column('password', sa.String, nullable = False)
    )


def downgrade():
    op.drop_table("user")
