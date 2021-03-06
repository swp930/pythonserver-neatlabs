"""empty message

Revision ID: 11b98d88a787
Revises: 78cc1765d2db
Create Date: 2019-05-24 15:33:50.402623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11b98d88a787'
down_revision = '78cc1765d2db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uniqueidentifier', sa.String(), nullable=True),
    sa.Column('waketime', sa.String(), nullable=True),
    sa.Column('sleeptime', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
