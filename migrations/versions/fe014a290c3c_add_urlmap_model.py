"""add URLMap model

Revision ID: fe014a290c3c
Revises: 
Create Date: 2024-10-10 21:42:45.087518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe014a290c3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=256), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short')
    )
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_url_map_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_url_map_timestamp'))

    op.drop_table('url_map')
    # ### end Alembic commands ###
