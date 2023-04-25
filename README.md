# PInREx DB Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/jdkern11/pinrex_db_models/workflows/tests/badge.svg)](https://github.com/jdkern11/pinrex_db_models/actions?workflow=tests)
[![codecov](https://codecov.io/gh/jdkern11/pinrex_db_models/branch/main/graph/badge.svg?token=4MU1H8MD94)](https://codecov.io/gh/jdkern11/pinrex_db_models)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![version](https://img.shields.io/badge/Release-3.3.3-blue)](https://github.com/jdkern11/pinrex_db_models/releases)


SQLAlchemy models to format PostgreSQL database for data.

## Upgrade
```bash
poetry run alembic revision --autogenerate -m "description of changes"
poetry run alembic upgrade head
```

## Bug when adding unique constrain
When adding a unique constraint, alembic won't register it when first creating the table.
To fix this, do the following AFTER running the revision, but BEFORE upgrading.

```Python
    op.create_table('reaction_steps',
    sa.Column('reaction_id', sa.Integer(), nullable=False),
    sa.Column('reaction_procedure_id', sa.Integer(), nullable=False),
    sa.Column('step', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['reaction_id'], ['reactions.id'], ),
    sa.ForeignKeyConstraint(['reaction_procedure_id'], ['reaction_procedures.id'], ),
    sa.PrimaryKeyConstraint('reaction_id', 'reaction_procedure_id', 'step'),
    # delete this sa.UniqueConstraint line
    sa.UniqueConstraint('reaction_procedure_id', 'reaction_id', 'step', name='unique_reaction_step')
    )
    # add this line instead
    # note, first variable is constraint name, next is table name, then list of columns
    op.create_unique_constraint('unique_reaction_step', 'reaction_steps', ['reaction_procedure_id', 'reaction_id', 'step'])
```
