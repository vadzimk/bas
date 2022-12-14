"""initial migration

Revision ID: b3d3d845272d
Revises: 
Create Date: 2022-08-03 20:59:22.288190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3d3d845272d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('rating', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('profile_url', sa.String(), nullable=True),
    sa.Column('overview', sa.String(), nullable=True),
    sa.Column('homepage_url', sa.String(), nullable=True),
    sa.Column('industry', sa.String(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('other_locations_employees', sa.String(), nullable=True),
    sa.Column('other_locations_employees_html', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_homepage_url'), 'company', ['homepage_url'], unique=False)
    op.create_index(op.f('ix_company_profile_url'), 'company', ['profile_url'], unique=False)
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('estimated_salary', sa.String(), nullable=True),
    sa.Column('salary', sa.String(), nullable=True),
    sa.Column('job_type', sa.String(), nullable=True),
    sa.Column('multiple_candidates', sa.String(), nullable=True),
    sa.Column('date_posted', sa.String(), nullable=True),
    sa.Column('qualifications', sa.String(), nullable=True),
    sa.Column('benefits', sa.String(), nullable=True),
    sa.Column('description_markdown', sa.String(), nullable=True),
    sa.Column('description_text', sa.String(), nullable=True),
    sa.Column('description_html', sa.String(), nullable=True),
    sa.Column('hiring_insights', sa.String(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_url'), 'job', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_job_url'), table_name='job')
    op.drop_table('job')
    op.drop_index(op.f('ix_company_profile_url'), table_name='company')
    op.drop_index(op.f('ix_company_homepage_url'), table_name='company')
    op.drop_table('company')
    # ### end Alembic commands ###
