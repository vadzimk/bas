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
    # Drop the foreign key constraint
    op.drop_constraint('search_task_id_fkey', 'search', type_='foreignkey')

    with op.batch_alter_table('task', schema=None) as batch_op:
        # Change the type of the primary key column
        batch_op.alter_column('id',
                              existing_type=sa.Integer(),
                              type_=sa.VARCHAR(),
                              existing_nullable=False,
                              postgresql_using="id::varchar",
                              )
    with op.batch_alter_table('search', schema=None) as batch_op:
        batch_op.alter_column('task_id',
                              existing_type=sa.Integer(),
                              type_=sa.VARCHAR(),
                              existing_nullable=False,
                              postgresql_using="task_id::varchar",
                              )
    # Re-create the foreign key constraint
    op.create_foreign_key('search_task_id_fkey', 'search', 'task', ['task_id'], ['id'])


def downgrade():
    # Drop the foreign key constraint
    op.drop_constraint('search_task_id_fkey', 'search', type_='foreignkey')

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('id',
                              existing_type=sa.VARCHAR(),
                              type_=sa.Integer(),
                              existing_nullable=False,
                              )
    with op.batch_alter_table('search', schema=None) as batch_op:
        batch_op.alter_column('task_id',
                              existing_type=sa.VARCHAR(),
                              type_=sa.Integer(),
                              existing_nullable=False,
                              )
    # Re-create the foreign key constraint
    op.create_foreign_key('search_task_id_fkey', 'search', 'task', ['task_id'], ['id'])

