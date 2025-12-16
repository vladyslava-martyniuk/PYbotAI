"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-15 20:41:04

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=140), nullable=False),
    )
    op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=False)

    op.create_table(
        "ai_api",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column("url", sa.String(length=255), nullable=False),
    )
    op.create_index(op.f("ix_ai_api_id"), "ai_api", ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=140), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("session", sa.String(length=255), nullable=True),
        sa.Column("is_banned", sa.Boolean(), nullable=True, server_default=sa.text("0")),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "ai_api_models",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("ai_api_id", sa.Integer(), sa.ForeignKey("ai_api.id"), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
    )
    op.create_index(op.f("ix_ai_api_models_id"), "ai_api_models", ["id"], unique=False)

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("ai_api_model_id", sa.Integer(), sa.ForeignKey("ai_api_models.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
    )
    op.create_index(op.f("ix_reviews_id"), "reviews", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_reviews_id"), table_name="reviews")
    op.drop_table("reviews")

    op.drop_index(op.f("ix_ai_api_models_id"), table_name="ai_api_models")
    op.drop_table("ai_api_models")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_ai_api_id"), table_name="ai_api")
    op.drop_table("ai_api")

    op.drop_index(op.f("ix_roles_id"), table_name="roles")
    op.drop_table("roles")
