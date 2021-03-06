"""empty message

Revision ID: 4bb267bf977a
Revises: 153b61318af6
Create Date: 2015-04-12 11:56:37.258000

"""

# revision identifiers, used by Alembic.
revision = '4bb267bf977a'
down_revision = '153b61318af6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('name', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'name')
    ### end Alembic commands ###
