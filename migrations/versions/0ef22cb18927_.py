"""empty message

Revision ID: 0ef22cb18927
Revises: 44ce800bf270
Create Date: 2019-05-27 20:42:56.979205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ef22cb18927'
down_revision = '44ce800bf270'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mooddata', sa.Column('datapoints', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mooddata', 'datapoints')
    # ### end Alembic commands ###
