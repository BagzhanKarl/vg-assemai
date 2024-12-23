"""Чуть обновление в моделях

Revision ID: 3991bc9ab6dc
Revises: 2acd0fbc88d7
Create Date: 2024-12-19 12:56:13.248249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3991bc9ab6dc'
down_revision = '2acd0fbc88d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('search_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('query', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search_data')
    # ### end Alembic commands ###
