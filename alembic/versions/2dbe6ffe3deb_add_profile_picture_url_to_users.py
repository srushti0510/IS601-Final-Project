"""Add profile_picture_url to users

Revision ID: 2dbe6ffe3deb
Revises: 25d814bc83ed
Create Date: 2025-05-05 19:27:39.269751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dbe6ffe3deb'
down_revision: Union[str, None] = '25d814bc83ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
