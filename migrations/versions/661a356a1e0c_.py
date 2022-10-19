"""empty message

Revision ID: 661a356a1e0c
Revises: b2917b48cc92
Create Date: 2022-10-10 13:35:22.681941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '661a356a1e0c'
down_revision = 'b2917b48cc92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournament', sa.Column('tournamentPicture', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournament', 'tournamentPicture')
    # ### end Alembic commands ###
