"""Task add state and info columns

Revision ID: 9a8c8cc91f12
Revises: ef40572e7580
Create Date: 2023-01-05 18:05:17.902448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a8c8cc91f12'
down_revision = 'ef40572e7580'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('info', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Task', schema=None) as batch_op:
        batch_op.drop_column('info')
        batch_op.drop_column('state')

    # ### end Alembic commands ###