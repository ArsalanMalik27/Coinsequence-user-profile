"""added student funds courses table to sync funds service data

Revision ID: 3f7ea0142716
Revises: 5986e6084992
Create Date: 2023-10-19 11:30:31.360145

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3f7ea0142716'
down_revision = '5986e6084992'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('studentfundcourses',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('college_id', sa.UUID(), nullable=True),
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.Column('college_name', sa.String(length=256), nullable=True),
    sa.Column('course_name', sa.String(length=256), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('userprofile', sa.Column('sub_ethinicity_id', sa.UUID(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userprofile', 'sub_ethinicity_id')
    op.drop_table('studentfundcourses')
    # ### end Alembic commands ###
