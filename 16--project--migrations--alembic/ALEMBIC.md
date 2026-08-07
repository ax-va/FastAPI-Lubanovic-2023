# Alembic

Alembic is a *database migration tool* for SQLAlchemy.

Its purpose is to *manage changes to the database schema over time*.

Without Alembic, every schema change would have to be applied manually using SQL statements
such as `CREATE TABLE`, `ALTER_TABLE`, or `DROP COLUMN`.

Instead, Alembic records each schema change as a migration, 
allowing every environment (development, testing, staging, and production)
to evolve the database in a controlled and reproducible way.

Typical schema changes includes:
- creating or dropping tables;
- adding, removing, or renaming columns;
- creating or dropping indexes;
- changing constraints;
- modifying relationships between tables.

ORM models describe what the schema should lock like.
Alembic changes the actual database to match those models.

## Migration and Migration Revision

- A *migration* is a change to the database schema.

- A *migration revision* is the Alembic file that records and applies one migration. 

## 1. Initialize Alembic

- Install Alembic
    ```shell
    $ pip install alembic
    ```
- Run `alembic init alembic`
    ```shell
    .../16--project--migrations--alembic$ alembic init alembic
    ```

## 2. Configure `alembic/env.py`

`env.py` is the entry point of Alembic - every Alembic command starts by executing this file.

- Import all ORM models.
- Import the application's `DATABASE_URL`.
- Import the application's `AsyncEngine`.
- Set `target_metadata`.
- Configure offline and online migration modes and call them.


Note:

Alembic uses the same asynchronous database driver and connection URL as the application.
Although migrations could be executed through a separate synchronous driver,
sharing a single configuration keeps the setup consistent and avoids configuration drift.

## Show the Current Database Revision

```shell
$ alembic current
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
```

This command verifies that:
- Alembic is configured correctly.
- `env.py` loads successfully.
- The database connection works.
- Alembic can read the `alembic_version` table.

If no migrations have been applied yet, no revision will be shown.

Note:

Connecting to a SQLite database automatically creates the database file if it does not already exist.
However, no tables are created until a migration is executed.

## Create a New Migration Revision
```shell
$ alembic revision -m "first test"
  Generating ...16--project--migrations--alembic/alembic/versions/b4c1016ff36d_first_test.py ...  done
```

This command does not execute a migration.
Instead, it creates a new migration revision - a Python file inside the `alembic/versions` directory.
This file contains empty `upgrade()` and `downgrade()` functions 
that you will fill in manually or generate automatically with `--autogenerate`.

Later, instead of creating an empty migration manually, 
we will use `--autogenerate` to let Alembic generate schema changes 
by comparing the ORM models with the current database schema.

At this point, the database schema remains unchanged unless `alembic upgrage head` is executed.

## 3. Create the Initial Database Schema

Instead of writing the migration manually,
Alembic can compare the ORM models with the current database schema
and generate the migration automatically.

Note:

Before creating a new migration with `--autogenerate`,
the database must already be at the latest migration revision.
Alembic does not allow autogeneration 
when there are unapplied migration revisions,
because it can no longer reliably compare 
the current database schema with the migration history.

Therefore, first delete the `b4c1016ff36d_first_test.py` file, then run

```shell
$ alembic revision --autogenerate -m "create initial schema"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.schemas
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.tables
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.types
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.constraints
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.defaults
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.comments
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.checkconstraint_byname
INFO  [alembic.autogenerate.compare.tables] Detected added table 'creatures'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'explorers'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'users'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'explorer_creature_relationship'
  Generating .../16--project--migrations--alembic/alembic/versions/2598b3f4b825_create_initial_schema.py ...  done
```

The ORM models have been compared with the current database schema 
and the migration file `598b3f4b825_create_initial_schema.py` has been generated.
The database has been not modified yet.

Note:

Autogenerated migrations should always be review before they are applied.
Alembic can generate references to SQLModel-specific types such as `sqlmodel.sql-sqltypes.AutoString()`.
But migration files should preferably use standard SQLAlchemy types.
This keeps migrations independent of ORM-specific implementation details and more stable over time.
In this case, replace `sqlmodel.sql-sqltypes.AutoString()` with `sa.String()`.

Apply the migration

```shell
$ $ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 2598b3f4b825, create initial schema
```

This command executes the `upgrade()` function of all pending migration revisions
and actually creates, modifies, or removes database objects.
In the usual `--autogenerate` workflow, each generated migration is applied 
before the next one is created, so there is typically only one pending migration revision.

Migration files stores the complete history of schema changes,
while the `alembic_version` table stores only the current revision of a particular database. 

## How Alembic Tracks Migration Order

Each migration file contains two important identifiers: 

- `revision` is the unique identifier of the current migration.
- `down_revision` identifies the migration that must be applied immediately before it.

Together, these identifiers form a chain of migration revisions.
Alembic does not determine the order from file names or timestamps.
Instead, it follows the `down_revision` links stored inside the migration files.

The current state of the database is stored in the `alembic_version` table.
It contains the `revision` identifier of the latest applied migration.

When running `alembic upgrade head`, Alembic starts from the current revision recorded in the database
and follows the chain forward, executing each pending `upgrade()` function,
until the latest revision (`head`) is reached.

When running `alembic downgrade -1`, Alembic executes the current migration's `downgrade()` function
and then updates the `alembic_version` table to the migration specified by `down_revision`.

Common revision targets:
- `head`: Update to the latest migration.
- `base`: Downgrade all the way to an empty database.
- `-1`: Downgrade one migration.
- `<revisipn_id>`: Upgrade or downgrade to a specific revision.

## 4. Typical Migration Workflow

1. Modify the ORM models.

2. Generate a new migration revision with `alembic revision --autogenerate -m "describe the schema change"`.

3. Review the generated migration and make any necessary adjustments.

4. Apply the migration with `alembic upgrade head`.

5. If necessary, roll back the last migration with `alembic downgrade -1`.

Each migration should represent a single logical schema change.
After applying it with `alembic upgrade head`, the database and the ORM models are synchronized again.