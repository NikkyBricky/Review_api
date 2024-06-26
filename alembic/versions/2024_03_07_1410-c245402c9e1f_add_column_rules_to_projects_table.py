"""add column rules to projects table

Revision ID: c245402c9e1f
Revises: 7aee713a7761
Create Date: 2024-03-07 14:10:09.959484

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c245402c9e1f"
down_revision: Union[str, None] = "7aee713a7761"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "projects",
        sa.Column(
            "rules",
            sa.String(),
            server_default="Это базовые критерии для ревью проектов. Они могут меняться от одного проекта к другому.Вы можете воспользоваться ими, если нужно. Правила:\n\n1. Код хорошо читается и понятно организован\n\n2. Функциональность проекта соответствует задаче заказчика.\n\n3. Код запускается и не выдает ошибку при попытке его запустить или как-либовзаимодействовать с ним.\n\n4. Присутствует документация к проекту.\n\n5. Функции реализованы без багов и работают так, как описаны в документации к проекту.",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("projects", "rules")
    # ### end Alembic commands ###
