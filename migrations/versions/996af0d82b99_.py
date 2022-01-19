"""empty message

Revision ID: 996af0d82b99
Revises: 03105a7ade02
Create Date: 2022-01-19 09:46:06.195362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '996af0d82b99'
down_revision = '03105a7ade02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###