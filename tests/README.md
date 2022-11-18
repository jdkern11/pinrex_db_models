# Testing
All helper functions are tested as well as any unique `__init__` definitions in the
models


## Environment Variables for Testing
In order to test, set the environment variables
```
PINREX_DB_USER
PINREX_DB_PASSWORD
PINREX_DB_HOST
PINREX_DB_PORT
PINREX_DB_NAME
```

This assumes you have access to a postgresql database. Port and password can be
blank if appropriate. Name can localhost if appropriate. The database used will be

```python
f"{PINREX_DB_NAME}_test"
```
