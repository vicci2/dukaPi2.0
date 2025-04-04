"""added a table

Revision ID: ebc07b490dde
Revises: fad21f0abc92
Create Date: 2025-01-24 15:13:40.425878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ebc07b490dde'
down_revision: Union[str, None] = 'fad21f0abc92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
  pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('companies_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='companies_pkey'),
    sa.UniqueConstraint('email', name='companies_email_key'),
    sa.UniqueConstraint('name', name='companies_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_companies_id', 'companies', ['id'], unique=False)
    op.create_table('vendors',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('vendors_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tel_no', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False, comment='Delivery/Return status'),
    sa.Column('createdAt', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='vendors_company_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='vendors_pkey'),
    sa.UniqueConstraint('email', name='vendors_email_key'),
    sa.UniqueConstraint('tel_no', name='vendors_tel_no_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_vendors_id', 'vendors', ['id'], unique=False)
    op.create_index('ix_vendors_company_id', 'vendors', ['company_id'], unique=False)
    op.create_table('tiers',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tiers_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tiers_pkey'),
    sa.UniqueConstraint('name', name='tiers_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_tiers_id', 'tiers', ['id'], unique=False)
    op.create_table('sales',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('inventory_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Quantity sold'),
    sa.Column('base_price', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Base price during sale'),
    sa.Column('selling_price', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Selling price during sale'),
    sa.Column('last_updated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('sale_date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False, comment='Sale status'),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='sales_company_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], name='sales_inventory_id_fkey', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name='sales_pkey')
    )
    op.create_index('ix_sales_inventory_id', 'sales', ['inventory_id'], unique=False)
    op.create_index('ix_sales_id', 'sales', ['id'], unique=False)
    op.create_index('ix_sales_company_id', 'sales', ['company_id'], unique=False)
    op.create_table('inventory',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Stock quantity available'),
    sa.Column('base_price', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Base price of the product'),
    sa.Column('selling_price', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Selling price of the product'),
    sa.Column('serial_no', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('last_updated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='inventory_company_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='inventory_product_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='inventory_pkey'),
    sa.UniqueConstraint('serial_no', name='inventory_serial_no_key')
    )
    op.create_index('ix_inventory_product_id', 'inventory', ['product_id'], unique=False)
    op.create_index('ix_inventory_id', 'inventory', ['id'], unique=False)
    op.create_index('ix_inventory_company_id', 'inventory', ['company_id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('tel_no', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('role', postgresql.ENUM('admin', 'manager', 'staff', 'user', name='userrole'), autoincrement=False, nullable=True),
    sa.Column('last_login', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='users_company_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('tel_no', name='users_tel_no_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('subscriptions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tier_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('transaction_code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='subscriptions_company_id_fkey'),
    sa.ForeignKeyConstraint(['tier_id'], ['tiers.id'], name='subscriptions_tier_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='subscriptions_pkey'),
    sa.UniqueConstraint('transaction_code', name='subscriptions_transaction_code_key')
    )
    op.create_index('ix_subscriptions_id', 'subscriptions', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('vendor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('serial_no', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('supplier', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('desc', sa.TEXT(), autoincrement=False, nullable=False, comment='Detailed product description'),
    sa.Column('quantity', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Stock quantity available'),
    sa.Column('b_p', sa.NUMERIC(), autoincrement=False, nullable=False, comment='Base price of the product'),
    sa.Column('last_updated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='products_company_id_fkey'),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], name='products_vendor_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='products_pkey'),
    sa.UniqueConstraint('product_name', name='products_product_name_key'),
    sa.UniqueConstraint('serial_no', name='products_serial_no_key')
    )
    op.create_index('ix_products_vendor_id', 'products', ['vendor_id'], unique=False)
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.create_index('ix_products_company_id', 'products', ['company_id'], unique=False)
    # ### end Alembic commands ###
