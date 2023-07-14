"""add initial tables

Revision ID: 403a2a92950c
Revises: 
Create Date: 2022-11-27 16:19:36.113404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '403a2a92950c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'proxy',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('ip', sa.String(255), nullable=False),
        sa.Column('port', sa.Integer, nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('proxy_type', sa.String(255), nullable=False),
        sa.Column('country', sa.String(255), nullable=False),
        sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('service_name', sa.String(255), nullable=False),
        sa.Column('job_names', sa.JSON, nullable=False),
        sa.Column('active', sa.Boolean, nullable=False),
    )


def downgrade():
    op.drop_table('proxy')
