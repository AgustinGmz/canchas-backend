"""initial

Revision ID: 1234567890ab
Revises: 
Create Date: 2026-07-31 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1234567890ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)
    op.create_index(op.f('ix_usuarios_nombre'), 'usuarios', ['nombre'], unique=False)

    op.create_table('canchas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('tipo', sa.String(), nullable=True),
    sa.Column('precio_hora', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_canchas_id'), 'canchas', ['id'], unique=False)
    op.create_index(op.f('ix_canchas_nombre'), 'canchas', ['nombre'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_canchas_nombre'), table_name='canchas')
    op.drop_index(op.f('ix_canchas_id'), table_name='canchas')
    op.drop_table('canchas')
    op.drop_index(op.f('ix_usuarios_nombre'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
