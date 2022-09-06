"""remove search_model.experience

Revision ID: 9143c56db953
Revises: 3ffc7a349a57
Create Date: 2022-08-28 00:25:53.027983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9143c56db953'
down_revision = '3ffc7a349a57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('search_model', schema=None) as batch_op:
        batch_op.drop_column('experience')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('search_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('experience', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###