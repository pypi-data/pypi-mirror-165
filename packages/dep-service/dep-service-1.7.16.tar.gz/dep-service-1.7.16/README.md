## Package "dep-service"
For easy creating web-apps with many features out-the-box.

### Service commands

Run service with uvicorn:
```shell script
python -m service run
```

Run tests:
```shell script
python -m service test
```

Generate locale.gen file
```shell script
python -m service locale-gen
```

Make a new migration:
```shell script
# if alembic used
python -m service make-migration --name add_new_field
```

Migrate:
```shell script
# if alembic used
python -m service migrate
```

Rollback migration:
```shell script
# if alembic used
python -m service rollback --name add_new_field
```
