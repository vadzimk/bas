"""added Job.created_str column

Revision ID: 8c98a1d12a05
Revises: 02fbdd452539
Create Date: 2022-08-05 12:47:28.025131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c98a1d12a05'
down_revision = '02fbdd452539'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('created_str', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'created_str')
    # ### end Alembic commands ###
