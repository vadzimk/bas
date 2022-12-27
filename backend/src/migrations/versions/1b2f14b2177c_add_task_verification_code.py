"""add task verification code

Revision ID: 1b2f14b2177c
Revises: ec7a3b51ac13
Create Date: 2022-11-14 02:14:35.273823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b2f14b2177c'
down_revision = 'ec7a3b51ac13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verification_code', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Task', schema=None) as batch_op:
        batch_op.drop_column('verification_code')

    # ### end Alembic commands ###