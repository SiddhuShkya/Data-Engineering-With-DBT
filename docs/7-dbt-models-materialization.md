# Materialization of DBT Models

So we've created our DBT models, but there's one small thing we need to consider is that how do we want our models to look like for our database users. You can achieve this using the materialization in dbt.

Materialization essentially controls how your models within your database are viewed and created. It does the following things:

- It limits what tables can be viewed by your database users.
- It reduces the cost of data storage by not having them materialized, but still available.
- It speeds up some data pipelines such as a dashboard so it doesn't have to wait for the query to run before you can actually get the data.

## Materialization Methods

DBT allows 5 different materialization methods:

- `Table:` Physically builds and stores the data as a table in the database on each run, replacing the previous version entirely.
- `View:` Creates a virtual table defined by the model's SQL query; data is not stored and is only computed when the view is queried.
- `Incremental:` Appends or updates only new/changed records since the last run, rather than rebuilding the entire table — ideal for large datasets where full refreshes are expensive.
- `Ephemeral:` Exists only as a CTE (Common Table Expression) injected into dependent models at runtime; it never materializes in the database at all.
- `Materialized View:` Similar to a view but the query result is physically stored and periodically refreshed by the database engine, combining the performance of a table with the freshness logic of a view.

For our project, we will only be dealing with table, view, and ephemeral, which places the data either persistently in storage, as a virtual query, or as a temporary in-query reference, respectively. Simply we are going to have the following:

- Our bronze data is going to be view.
- Our silver data is going to be ephemeral for the initial tables, because they're just used to help us for our final tables, which are going to be view, so we don't want our users to see it.
- And finally, our gold tables are going to be materialized as tables because their metrics being used by downstream people. So we want that data available as quickly as possible. 

Now, let's hop in into our DBT project.

## Implement Materialization into our DBT Project.

Now that we know what to set up for our materialization for our project, we have to go to the DBT project YAML file once again to setup our configurations.

1. We are going to updating the below models part of the dbt_project.yaml file.

```yml
models:
  nyc_parking_violations:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: view
```

2. Replace the above section with the below configuration using copy paste.

```yml
models:
  nyc_parking_violations:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: ephemeral
    bronze:
      +materialized: view
    silver:
      silver_parking_violation_codes:
        +materialized: ephemeral
      silver_parking_violations:
        +materialized: ephemeral
      silver_violation_tickets:
        +materialized: view
      silver_violation_vehicles:
        +materialized: view
    gold:
      +materialized: table
```

*After updating the dbt_project.yml file, run your dbt and see what it looks like.*

- Make sure you are in the right folder.

```sh
$ cd nyc_parking_violations/
```

- Run dbt debug.

```sh
$ dbt debug
```
```sh
08:10:00  Running with dbt=1.8.9
08:10:00  dbt version: 1.8.9
08:10:00  python version: 3.11.15
08:10:00  python path: /home/siddhu/Desktop/Data-Engineering-With-DBT/venv/bin/python3.11
08:10:00  os info: Linux-6.14.0-37-generic-x86_64-with-glibc2.39
08:10:00  Using profiles dir at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations
08:10:00  Using profiles.yml file at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations/profiles.yml
08:10:00  Using dbt_project.yml file at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations/dbt_project.yml
08:10:00  adapter type: duckdb
08:10:00  adapter version: 1.8.4
08:10:00  Configuration:
08:10:00    profiles.yml file [OK found and valid]
08:10:00    dbt_project.yml file [OK found and valid]
08:10:00  Required dependencies:
08:10:00   - git [OK found]

08:10:00  Connection:
08:10:00    database: nyc_parking_violations
08:10:00    schema: main
08:10:00    path: ../data/nyc_parking_violations.db
08:10:00    config_options: None
08:10:00    extensions: None
08:10:00    settings: {}
08:10:00    external_root: .
08:10:00    use_credential_provider: None
08:10:00    attach: None
08:10:00    filesystems: None
08:10:00    remote: None
08:10:00    plugins: None
08:10:00    disable_transactions: False
08:10:00  Registered adapter: duckdb=1.8.4
08:10:00    Connection test: [OK connection ok]

08:10:00  All checks passed!
```

- Run dbt compile.

```sh
$ dbt compile
```

```sh
08:13:37  Running with dbt=1.8.9
08:13:37  Registered adapter: duckdb=1.8.4
08:13:37  Unable to do partial parsing because a project config has changed
08:13:38  Found 10 models, 426 macros
08:13:38  
08:13:38  Concurrency: 1 threads (target='dev')
08:13:38  
```

- Finall dbt run.

```sh
$ dbt run
```
```sh
08:14:31  Running with dbt=1.8.9
08:14:31  Registered adapter: duckdb=1.8.4
08:14:31  Found 10 models, 426 macros
08:14:31  
08:14:31  Concurrency: 1 threads (target='dev')
08:14:31  
08:14:31  1 of 6 START sql view model main.bronze_parking_violation_codes ................ [RUN]
08:14:31  1 of 6 OK created sql view model main.bronze_parking_violation_codes ........... [OK in 0.08s]
08:14:31  2 of 6 START sql view model main.bronze_parking_violations ..................... [RUN]
08:14:31  2 of 6 OK created sql view model main.bronze_parking_violations ................ [OK in 0.04s]
08:14:31  3 of 6 START sql view model main.silver_violation_tickets ...................... [RUN]
08:14:32  3 of 6 OK created sql view model main.silver_violation_tickets ................. [OK in 0.12s]
08:14:32  4 of 6 START sql view model main.silver_violation_vehicles ..................... [RUN]
08:14:32  4 of 6 OK created sql view model main.silver_violation_vehicles ................ [OK in 0.04s]
08:14:32  5 of 6 START sql table model main.gold_ticket_metrics .......................... [RUN]
08:14:32  5 of 6 OK created sql table model main.gold_ticket_metrics ..................... [OK in 0.07s]
08:14:32  6 of 6 START sql table model main.gold_vehicle_metrics ......................... [RUN]
08:14:32  6 of 6 OK created sql table model main.gold_vehicle_metrics .................... [OK in 0.04s]
08:14:32  
08:14:32  Finished running 4 view models, 2 table models in 0 hours 0 minutes and 0.54 seconds (0.54s).
08:14:32  
08:14:32  Completed successfully
08:14:32  
08:14:32  Done. PASS=6 WARN=0 ERROR=0 SKIP=0 TOTAL=6
```

*You could see from the above logs that we don't have models that were materialized as ephemeral. So we know that our materialization is working.*

---

<div align="center">

<h2>✦ Thank You For Reading This Guide ✦</h2>

> *May your pipelines never break and your queries always run fast.* 🚀

</div>