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
