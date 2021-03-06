"""empty message

Revision ID: 67974b131c91
Revises: 
Create Date: 2017-06-18 18:52:23.362451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67974b131c91'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bucketlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bucketlist_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('bucketlist_id', sa.Integer(), nullable=True),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['bucketlist_id'], ['bucketlist.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bucketlist_item')
    op.drop_table('bucketlist')
    op.drop_table('user_model')
    # ### end Alembic commands ###
