"""creating tables and first setup on clinicdb

Revision ID: 720f1c44a9d5
Revises: 
Create Date: 2023-05-17 11:11:25.353600

"""
from alembic import op
import sqlalchemy as sa
from dbtest2 import create_tables


# revision identifiers, used by Alembic.
revision = "720f1c44a9d5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    create_tables()
    pass


def downgrade() -> None:
    pass
