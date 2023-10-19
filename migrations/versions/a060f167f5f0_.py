"""empty message

Revision ID: a060f167f5f0
Revises: 
Create Date: 2023-10-19 18:27:55.312682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a060f167f5f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_image',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_image')
    # ### end Alembic commands ###
