"""create applications and query_definitions

Revision ID: d73c4f4a6d60
Revises: 24faa6e1fe5e
Create Date: 2025-05-21 13:41:16.179049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd73c4f4a6d60'
down_revision: Union[str, None] = '24faa6e1fe5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('blob_connection_string', sa.String(), nullable=False),
    sa.Column('blob_container', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('query_definitions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('sql_template', sa.String(), nullable=False),
    sa.Column('db_url', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['applications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('query_definitions')
    op.drop_table('applications')
    # ### end Alembic commands ###
