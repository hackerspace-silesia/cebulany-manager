"""empty message

Revision ID: 9f2d247b886a
Revises: 2c9cce8a50b1
Create Date: 2025-03-16 17:53:39.776675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2d247b886a'
down_revision = '2c9cce8a50b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accountancytype',
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('color', sa.String(length=6), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_accountancytype'))
    )
    op.create_index(op.f('ix_accountancytype_name'), 'accountancytype', ['name'], unique=False)
    op.create_table('innerbudget',
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('color', sa.String(length=6), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_innerbudget'))
    )
    op.create_index(op.f('ix_innerbudget_name'), 'innerbudget', ['name'], unique=False)
    op.add_column('budget', sa.Column('description', sa.String(length=300), server_default='', nullable=False))
    op.add_column('payment', sa.Column('inner_budget_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_payment_inner_budget_id_innerbudget'), 'payment', 'innerbudget', ['inner_budget_id'], ['id'])
    op.add_column('paymenttype', sa.Column('accountancy_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_paymenttype_accountancy_type_id_accountancytype'), 'paymenttype', 'accountancytype', ['accountancy_type_id'], ['id'])
    op.add_column('transaction', sa.Column('additional_info', sa.String(length=300), server_default='', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'additional_info')
    op.drop_constraint(op.f('fk_paymenttype_accountancy_type_id_accountancytype'), 'paymenttype', type_='foreignkey')
    op.drop_column('paymenttype', 'accountancy_type_id')
    op.drop_constraint(op.f('fk_payment_inner_budget_id_innerbudget'), 'payment', type_='foreignkey')
    op.drop_column('payment', 'inner_budget_id')
    op.drop_column('budget', 'description')
    op.drop_index(op.f('ix_innerbudget_name'), table_name='innerbudget')
    op.drop_table('innerbudget')
    op.drop_index(op.f('ix_accountancytype_name'), table_name='accountancytype')
    op.drop_table('accountancytype')
    # ### end Alembic commands ###
