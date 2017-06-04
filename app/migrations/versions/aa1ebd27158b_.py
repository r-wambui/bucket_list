"""empty message

Revision ID: aa1ebd27158b
Revises: 1d6a059bd598
Create Date: 2017-05-31 09:06:27.664296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa1ebd27158b'
down_revision = '1d6a059bd598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bucketlist')
    op.drop_table('bucketlist_item')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=30), nullable=True),
    sa.Column('password', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bucketlist_item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('date_modified', sa.DATETIME(), nullable=True),
    sa.Column('created_by', sa.INTEGER(), nullable=True),
    sa.Column('bucketlist_id', sa.INTEGER(), nullable=True),
    sa.Column('done', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('done IN (0, 1)'),
    sa.ForeignKeyConstraint(['bucketlist_id'], ['bucketlist.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bucketlist',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('date_modified', sa.DATETIME(), nullable=True),
    sa.Column('created_by', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###