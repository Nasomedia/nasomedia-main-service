"""delete profile column in publisher table

Revision ID: 64343ba48eae
Revises: 009943f92899
Create Date: 2021-11-09 14:29:57.754631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64343ba48eae'
down_revision = '009943f92899'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publisher', 'profile_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publisher', sa.Column('profile_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
