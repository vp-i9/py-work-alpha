"""adding two new columns to products table: last_modified_date and last_modified_quantity

Revision ID: 41cb3c4776f5
Revises: 720f1c44a9d5
Create Date: 2023-05-17 12:58:12.129657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41cb3c4776f5"
down_revision = "720f1c44a9d5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("products", sa.Column("last_modified_date", sa.DateTime))
    op.add_column("products", sa.Column("last_modified_quantity", sa.Integer))
    pass


def downgrade() -> None:
    op.drop_column("products", "last_modified_date")
    op.drop_column("products", "last_modified_quantity")
    pass
