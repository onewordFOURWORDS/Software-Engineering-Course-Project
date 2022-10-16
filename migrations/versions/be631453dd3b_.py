"""empty message

Revision ID: be631453dd3b
Revises: 6b024780b6f5
Create Date: 2022-10-12 22:21:46.251224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be631453dd3b'
down_revision = '6b024780b6f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'league', ['leagueName'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'league', type_='unique')
    # ### end Alembic commands ###
