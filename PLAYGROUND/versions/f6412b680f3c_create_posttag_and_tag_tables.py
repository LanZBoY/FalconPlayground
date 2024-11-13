"""create PostTag and Tag Tables

Revision ID: f6412b680f3c
Revises: 284f5ef2f268
Create Date: 2024-11-13 10:10:17.459976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6412b680f3c'
down_revision = '284f5ef2f268'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer, primary_key = True),
        sa.Column("name", sa.String, nullable = False)
    )
    op.create_table(
        "post_tag_relation",
        sa.Column("post_id", sa.Integer, sa.ForeignKey("post.id")),
        sa.Column("tag_id", sa.Integer, sa.ForeignKey("tag.id"))
    )


def downgrade():
    op.drop_table("tag")
    op.drop_table("post_tag_relation")
