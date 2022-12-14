"""add Job, Company timestamp_created, timestamp_updated

Revision ID: 954337b597a8
Revises: 4f07fe41c48b
Create Date: 2022-09-05 19:45:53.961655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954337b597a8'
down_revision = '4f07fe41c48b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp_created', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('timestamp_updated', sa.DateTime(), nullable=True))

    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp_created', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('timestamp_updated', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_column('timestamp_updated')
        batch_op.drop_column('timestamp_created')

    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_column('timestamp_updated')
        batch_op.drop_column('timestamp_created')

    # ### end Alembic commands ###
