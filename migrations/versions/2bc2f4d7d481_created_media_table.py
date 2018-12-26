"""created media table

Revision ID: 2bc2f4d7d481
Revises: f3dace20992c
Create Date: 2018-12-27 01:13:17.508193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc2f4d7d481'
down_revision = 'f3dace20992c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('medium_name', sa.Text(), nullable=False),
    sa.Column('medium_url', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media')
    # ### end Alembic commands ###
