"""initial_mig

Revision ID: 6f0e8fff647c
Revises: 
Create Date: 2023-02-17 17:10:31.703376

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6f0e8fff647c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('suburb', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userprofile',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('profile_type', sa.Enum('STUDENT', 'INVESTOR', 'TEACHER', 'PARENT', name='userprofiletype'), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('gender', sa.Enum('male', 'female', 'non_binary', 'other', name='gender'), nullable=True),
    sa.Column('nationality', sa.String(length=255), nullable=True),
    sa.Column('headline', sa.String(length=255), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('hobbies', postgresql.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('profile_image', sa.String(length=255), nullable=True),
    sa.Column('profile_image_thumbnail', sa.String(length=255), nullable=True),
    sa.Column('pronoun', sa.String(length=255), nullable=True),
    sa.Column('legal_name', sa.String(length=255), nullable=True),
    sa.Column('ethinicity', sa.String(length=255), nullable=True),
    sa.Column('sub_ethinicity', sa.String(length=255), nullable=True),
    sa.Column('connection_count', sa.Integer(), nullable=True),
    sa.Column('karmapost_count', sa.Integer(), nullable=True),
    sa.Column('karmavalidation_count', sa.Integer(), nullable=True),
    sa.Column('karma_time', sa.Integer(), nullable=True),
    sa.Column('karma_coin', sa.Integer(), nullable=True),
    sa.Column('parent_code', sa.String(length=6), nullable=True),
    sa.Column('ethinicity_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('activity_name', sa.String(length=255), nullable=True),
    sa.Column('activity_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('activity_type', sa.Enum('ACADEMIC', 'EXTRA_CURRICULAR', name='activitytype'), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('award',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('recognition_type', sa.Enum('SCHOOL', 'STATE', 'NATIONAL', 'INTERNATIONAL', name='recognitiontype'), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('grade', sa.Enum('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', name='gradetype'), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('childrenprofile',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('child_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collegeuniversities',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('degree', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('university_name', sa.String(length=255), nullable=True),
    sa.Column('university_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connectionconnection',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('user_a', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_b', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_parent', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_a'], ['userprofile.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_b'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connectionrequestconnection',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('sender_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('receiver_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='connectionrequeststatus'), nullable=True),
    sa.Column('is_parent', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('education',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('institution_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('institution', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('is_current', sa.Boolean(), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('address_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('school_city', sa.String(length=256), nullable=True),
    sa.Column('school_state', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grade',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('institution_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('institution', sa.String(length=255), nullable=True),
    sa.Column('level', sa.String(length=255), nullable=True),
    sa.Column('gpa', sa.String(length=255), nullable=True),
    sa.Column('max_gpa', sa.String(length=255), nullable=True),
    sa.Column('courses', postgresql.ARRAY(sa.String(length=255)), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profileprivacy',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('profile_section_type', sa.Enum('PERSONAL', 'EDUCATION', 'SCORE', 'GRADE', 'AWARD', 'COLLEGE', 'LEADERSHIP', 'VOLUNTARY_WORK', 'INTERNSHIP', 'ACTIVITY', name='profilesectiontype'), nullable=True),
    sa.Column('privacy_type', sa.Enum('PRIVATE', 'CONNECTION', 'PUBLIC', name='privacytype'), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('participation_time_type', sa.Enum('DURING_SCHOOL_YEAR', 'DURING_SCHOOL_BREAK', 'ALL_YEAR', name='participationtimetype'), nullable=True),
    sa.Column('hours_spent', sa.String(length=255), nullable=True),
    sa.Column('grade', sa.Enum('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', name='gradetype'), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('test_name', sa.String(length=255), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('test_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('voluntary',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('hours', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('work',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('work_type', sa.Enum('PAID_INTERNSHIP', 'UNPAID_INTERNSHIP', 'PAID_WORK', name='worktype'), nullable=True),
    sa.Column('net_hours', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('score',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('profile_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('subject_name', sa.String(length=255), nullable=True),
    sa.Column('score', sa.String(length=200), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('activated_at', sa.DateTime(), nullable=True),
    sa.Column('subject_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('test_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['userprofile.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score')
    op.drop_table('work')
    op.drop_table('voluntary')
    op.drop_table('test')
    op.drop_table('roles')
    op.drop_table('profileprivacy')
    op.drop_table('grade')
    op.drop_table('education')
    op.drop_table('connectionrequestconnection')
    op.drop_table('connectionconnection')
    op.drop_table('collegeuniversities')
    op.drop_table('childrenprofile')
    op.drop_table('award')
    op.drop_table('activity')
    op.drop_table('userprofile')
    op.drop_table('address')
    # ### end Alembic commands ###
