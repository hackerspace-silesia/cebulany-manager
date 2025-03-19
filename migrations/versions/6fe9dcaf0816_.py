"""empty message

Revision ID: 6fe9dcaf0816
Revises: 78b153fa548c
Create Date: 2025-03-16 21:00:37.806949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fe9dcaf0816'
down_revision = '78b153fa548c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('suggestion', sa.Column('inner_budget_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_suggestion_inner_budget_id_innerbudget'), 'suggestion', 'innerbudget', ['inner_budget_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_suggestion_inner_budget_id_innerbudget'), 'suggestion', type_='foreignkey')
    op.drop_column('suggestion', 'inner_budget_id')
    # ### end Alembic commands ###
