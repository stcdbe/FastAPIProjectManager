"""Initial

Revision ID: 63357902409c
Revises: 
Create Date: 2024-04-28 20:22:48.371486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '63357902409c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('job_title', sa.String(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('sex', sa.Enum('m', 'f', name='usersex'), nullable=True),
    sa.Column('join_date', sa.DateTime(), nullable=False),
    sa.Column('guid', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_guid'), 'user', ['guid'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('project',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('tech_stack', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('constraint_date', sa.DateTime(), nullable=False),
    sa.Column('creator_guid', sa.Uuid(), nullable=False),
    sa.Column('mentor_guid', sa.Uuid(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('guid', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['creator_guid'], ['user.guid'], ),
    sa.ForeignKeyConstraint(['mentor_guid'], ['user.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_project_guid'), 'project', ['guid'], unique=False)
    op.create_table('task',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('is_completed', sa.Boolean(), nullable=False),
    sa.Column('project_guid', sa.Uuid(), nullable=False),
    sa.Column('executor_guid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('guid', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['executor_guid'], ['user.guid'], ),
    sa.ForeignKeyConstraint(['project_guid'], ['project.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_task_guid'), 'task', ['guid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_guid'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_project_guid'), table_name='project')
    op.drop_table('project')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_guid'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
