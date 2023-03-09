# PInREx DB Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/jdkern11/pinrex_db_models/workflows/tests/badge.svg)](https://github.com/jdkern11/pinrex_db_models/actions?workflow=tests)
[![codecov](https://codecov.io/gh/jdkern11/pinrex_db_models/branch/main/graph/badge.svg?token=4MU1H8MD94)](https://codecov.io/gh/jdkern11/pinrex_db_models)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![version](https://img.shields.io/badge/Release-2.0.0-blue)](https://github.com/jdkern11/pinrex_db_models/releases)


SQLAlchemy models to format PostgreSQL database for data.

## Upgrade
```bash
poetry run alembic revision --autogenerate -m "description of changes"
poetry run alembic upgrade head
```
