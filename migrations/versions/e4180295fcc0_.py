"""empty message

Revision ID: e4180295fcc0
Revises: 2a73402b0887
Create Date: 2025-11-05 17:15:46.569009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4180295fcc0'
down_revision = '2a73402b0887'
branch_labels = None
depends_on = None

inner_budget = sa.table('innerbudget',
    sa.column('id', sa.Integer),
    sa.column('name', sa.String),
    sa.column('color', sa.String),
)

inner_transfer = sa.table('innertransfer',
    sa.column('from_id', sa.Integer),
    sa.column('to_id', sa.Integer),
)

payment = sa.table('payment',
    sa.column('inner_budget_id', sa.Integer),
)

suggestion = sa.table('suggestion',
    sa.column('inner_budget_id', sa.Integer),
)

def upgrade():
    connection = op.get_bind()
    ret = connection.execute(
        inner_budget.insert().values({
            "name": "GŁÓWNY",
            "color": "000000",
        }).returning(inner_budget.c.id)
    )
    inner_budget_id = ret.scalar()

    a = op.execute(
        inner_transfer.update()
        .where(inner_transfer.c.from_id == None)
        .values({"from_id": inner_budget_id})
    )

    b= op.execute(
        inner_transfer.update()
        .where(inner_transfer.c.to_id == None)
        .values({"to_id": inner_budget_id})
    )

    op.execute(
        payment.update()
        .where(payment.c.inner_budget_id == None)
        .values({"inner_budget_id": inner_budget_id})
    )

    op.execute(
        suggestion.update()
        .where(suggestion.c.inner_budget_id == None)
        .values({"inner_budget_id": inner_budget_id})
    )

    op.alter_column('innertransfer', 'from_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('innertransfer', 'to_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('payment', 'inner_budget_id',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade():
    op.alter_column('payment', 'inner_budget_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('innertransfer', 'to_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('innertransfer', 'from_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.execute(
        inner_budget.delete().where(inner_budget.c.name == "GŁÓWNY")
    )
