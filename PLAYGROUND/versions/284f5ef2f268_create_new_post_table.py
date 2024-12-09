"""Create New Post Table

Revision ID: 284f5ef2f268
Revises: c34a931382eb
Create Date: 2024-11-10 14:38:32.252785

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "284f5ef2f268"
down_revision = "c34a931382eb"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post",
        sa.Column("user_id", sa.Integer),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
    )
    op.create_foreign_key("fk_post_user", "post", "user", ["user_id"], ["id"])


def downgrade():
    op.drop_constraint("fk_post_user", "post")
    op.drop_table("post")
