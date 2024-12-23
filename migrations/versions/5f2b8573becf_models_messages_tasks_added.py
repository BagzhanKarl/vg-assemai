"""Models messages tasks added

Revision ID: 5f2b8573becf
Revises: 2f9d6839c4e2
Create Date: 2024-12-19 12:54:03.078706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f2b8573becf'
down_revision = '2f9d6839c4e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('tokens', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=25), nullable=True),
    sa.Column('tasktype', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('messages')
    # ### end Alembic commands ###
