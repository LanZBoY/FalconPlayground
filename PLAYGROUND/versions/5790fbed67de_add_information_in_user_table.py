"""add information in user table

Revision ID: 5790fbed67de
Revises: b467818e93ec
Create Date: 2024-11-08 16:34:03.533517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5790fbed67de'
down_revision = 'b467818e93ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user",
                  sa.Column("email", sa.String)
                  )
    op.add_column("user",
                  sa.Column("address", sa.String)
                  )


def downgrade():
    op.drop_column("user", "email")
    op.drop_column("user", "address")
