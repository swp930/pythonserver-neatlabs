"""empty message

Revision ID: aaceebca7457
Revises: dcf6cdd3d12e
Create Date: 2019-05-31 17:19:11.651426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaceebca7457'
down_revision = 'dcf6cdd3d12e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userdata', sa.Column('enddate', sa.String(), nullable=True))
    op.add_column('userdata', sa.Column('startdate', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userdata', 'startdate')
    op.drop_column('userdata', 'enddate')
    # ### end Alembic commands ###
