"""next test adding data 1

Revision ID: 1cc73c938029
Revises: 41cb3c4776f5
Create Date: 2023-05-18 13:48:50.726514

"""
from alembic import op
import sqlalchemy as sa
from dbtest2 import add_data

# revision identifiers, used by Alembic.
revision = "1cc73c938029"
down_revision = "41cb3c4776f5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    add_data()
    pass


def downgrade() -> None:
    pass
