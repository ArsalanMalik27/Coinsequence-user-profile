"""added application table

Revision ID: 3d2884972404
Revises: cb5e67c9d120
Create Date: 2023-05-25 05:26:30.300836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d2884972404'
down_revision = 'cb5e67c9d120'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('profile_id', sa.UUID(), nullable=True),
    sa.Column('college_course_id', sa.UUID(), nullable=True),
    sa.Column('course_name', sa.String(), nullable=True),
    sa.Column('course_fees', sa.Integer(), nullable=True),
    sa.Column('course_duration', sa.Integer(), nullable=True),
    sa.Column('college_id', sa.UUID(), nullable=True),
    sa.Column('college_name', sa.String(), nullable=True),
    sa.Column('college_city', sa.String(), nullable=True),
    sa.Column('college_state', sa.String(), nullable=True),
    sa.Column('preference', sa.Integer(), nullable=True),
    sa.Column('reason', sa.String(), nullable=True),
    sa.Column('required_funds', sa.Integer(), nullable=True),
    sa.Column('admission_status', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('application')
    # ### end Alembic commands ###
