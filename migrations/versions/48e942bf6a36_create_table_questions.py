"""Create table Questions

Revision ID: 48e942bf6a36
Revises: 
Create Date: 2023-10-16 23:03:30.253457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48e942bf6a36'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('question_id', sa.UUID(), nullable=True),
    sa.Column('question_text', sa.Text(), nullable=False),
    sa.Column('question_answer', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('question_id', name='questions_question_id_pk'),
    sa.UniqueConstraint('question_text')
    )
    op.create_index('questions_text_idx', 'questions', ['question_text'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('questions_text_idx', table_name='questions')
    op.drop_table('questions')
    # ### end Alembic commands ###
