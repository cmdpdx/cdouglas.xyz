"""remove SimpleTitle table; 

Revision ID: a7ac3bea0cd4
Revises: 3ef80e9d85cc
Create Date: 2019-03-07 05:17:09.830765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7ac3bea0cd4'
down_revision = '3ef80e9d85cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_simple_title_text', table_name='simple_title')
    op.drop_table('simple_title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('simple_title',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=100), nullable=False),
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_simple_title_text', 'simple_title', ['text'], unique=1)
    # ### end Alembic commands ###