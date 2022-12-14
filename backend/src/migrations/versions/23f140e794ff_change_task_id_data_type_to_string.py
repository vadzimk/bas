"""change task id data type to string

Revision ID: 23f140e794ff
Revises: 954337b597a8
Create Date: 2022-09-23 12:28:01.794380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23f140e794ff'
down_revision = '954337b597a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_board_name', sa.String(), nullable=True),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('search_model_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.ForeignKeyConstraint(['search_model_id'], ['search_model.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search')
    op.drop_table('task')
    # ### end Alembic commands ###
