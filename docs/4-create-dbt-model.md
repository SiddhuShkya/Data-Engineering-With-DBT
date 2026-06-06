# Create a DBT Model

We are now going to create our first dbt model. When we ran dbt init, it created 2 example DBT models within directory. 

```text
.
├── analyses
├── dbt_project.yml
├── .gitignore
├── logs
├── macros
├── models
│   └── example  <--------------------- # Your auto generated model here.
│       ├── my_first_dbt_model.sql
│       ├── my_second_dbt_model.sql
│       └── schema.yml
├── profiles.yml
├── README.md
├── seeds
├── snapshots
└── tests
```

*You can completely remove the example folder, as this can make things confusing while creating your own dbt model.*

### 1. Create your first dbt model

- Go inside the models directory and create a new sql file called first_model.sql

```sh
$ cd nyc_parking_violations/
$ cd models
$ touch first_model.sql
```

> [!NOTE]
> A DBT Model is essentially just an SQL file. DBT sees the sql file and runs it through our system. 


- Copy paste the below SQL query to the first_model.sql

```sql
SELECT * FROM parking_violation_codes;
```

*This might seem very simple but as you start to scale multiple files, being able to structure it in a directory like this makes it so much easire to manage.*

### 2. Run your model using the dbt CLI commands.

Now that we have created our first dbt model, we can actually run it through the DBT project. There are 3 main commands that you can use to run your dbt models.

> [!IMPORTANT]
> Make sure that you have to be inside you DBT directory while running the below commands

- First Command

```sh
$ dbt debug
```

```sh
10:42:20  Running with dbt=1.8.9
10:42:21  dbt version: 1.8.9
10:42:21  python version: 3.11.15
10:42:21  python path: /home/siddhu/Desktop/Data-Engineering-With-DBT/venv/bin/python3.11
10:42:21  os info: Linux-6.14.0-37-generic-x86_64-with-glibc2.39
10:42:21  Using profiles dir at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations
10:42:21  Using profiles.yml file at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations/profiles.yml
10:42:21  Using dbt_project.yml file at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations/dbt_project.yml
10:42:21  adapter type: duckdb
10:42:21  adapter version: 1.8.4
10:42:21  Configuration:
10:42:21    profiles.yml file [OK found and valid]
10:42:21    dbt_project.yml file [OK found and valid]
10:42:21  Required dependencies:
10:42:21   - git [OK found]

10:42:21  Connection:
10:42:21    database: memory
10:42:21    schema: main
10:42:21    path: :memory:
10:42:21    config_options: None
10:42:21    extensions: None
10:42:21    settings: {}
10:42:21    external_root: .
10:42:21    use_credential_provider: None
10:42:21    attach: None
10:42:21    filesystems: None
10:42:21    remote: None
10:42:21    plugins: None
10:42:21    disable_transactions: False
10:42:21  Registered adapter: duckdb=1.8.4
10:42:21    Connection test: [OK connection ok]

10:42:21  All checks passed!
```

- Second Command

```sh
$ dbt compile
```
```sh
10:44:00  Running with dbt=1.8.9
10:44:01  Registered adapter: duckdb=1.8.4
10:44:01  Unable to do partial parsing because saved manifest not found. Starting full parse.
10:44:01  [WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 1 unused configuration paths:
- models.nyc_parking_violations.example
10:44:02  Found 1 model, 426 macros
10:44:02  
10:44:02  Concurrency: 1 threads (target='dev')
10:44:02 
```

*The above command runs all the models end-to-end, but doesn't execute the model SQL code nor materialize the tables, which is useful for quickly checking if your dbt models have any errors. In a large scale projects you can run this to check for errors a bit early.*

- Third Command

```sh
$ dbt run
```
```sh
10:48:43  Running with dbt=1.8.9
10:48:43  Registered adapter: duckdb=1.8.4
10:48:43  [WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 1 unused configuration paths:
- models.nyc_parking_violations.example
10:48:43  Found 1 model, 426 macros
10:48:43  
10:48:43  Concurrency: 1 threads (target='dev')
10:48:43  
10:48:43  1 of 1 START sql view model main.first_model ................................... [RUN]
10:48:43  1 of 1 ERROR creating sql view model main.first_model .......................... [ERROR in 0.05s]
10:48:43  
10:48:43  Finished running 1 view model in 0 hours 0 minutes and 0.14 seconds (0.14s).
10:48:43  
10:48:43  Completed with 1 error and 0 warnings:
10:48:43  
10:48:43    Runtime Error in model first_model (models/first_model.sql)
  Catalog Error: Table with name parking_violation_codes does not exist!
  Did you mean "pg_constraint"?
  LINE 5:     SELECT * FROM parking_violation_codes
                            ^
10:48:43  
10:48:43  Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1
```

*You should run into an error when you execute the above dbt run command, this is intentional. To understand why this is happending you should go back and see your profiles.yml file*

```yml
nyc_parking_violations:
  target: dev        
  outputs:
    dev: 
      type: duckdb
```

We have nyc_parking_violations and type as duckdb which is how it should be for this project. But this profiles.yml file doesn't know where to look, which is the database we created previously inside the data directory. Update the profiles.yml file to match the below and run the command again.

```yml
nyc_parking_violations:
  target: dev        
  outputs:
    dev: 
      type: duckdb
      path: '../data/nyc_parking_violations.db'
```

Update the profiles.yml file based on the above configuation and run the dbt run command again.

```sh
$ dbt run
```
```sh
10:57:10  Running with dbt=1.8.9
10:57:10  Registered adapter: duckdb=1.8.4
10:57:11  Unable to do partial parsing because profile has changed
10:57:11  [WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 1 unused configuration paths:
- models.nyc_parking_violations.example
10:57:11  Found 1 model, 426 macros
10:57:11  
10:57:11  Concurrency: 1 threads (target='dev')
10:57:11  
10:57:11  1 of 1 START sql view model main.first_model ................................... [RUN]
10:57:11  1 of 1 OK created sql view model main.first_model .............................. [OK in 0.07s]
10:57:11  
10:57:11  Finished running 1 view model in 0 hours 0 minutes and 0.19 seconds (0.19s).
10:57:12  
10:57:12  Completed successfully
10:57:12  
10:57:12  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1
```

### 3. Check the model output

- Go to your run-queries.ipynb notebook file and run the below block of code in a new cell. You should see a new table alongside nyc_parking_violations_2025 and nyc_parking_violation_codes.

```python
sql_query = """
show tables; 
"""

with ddb.connect("data/nyc_parking_violations.db") as con:
    display(con.sql(sql_query).df())
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>first_model</td>
    </tr>
    <tr>
      <th>1</th>
      <td>parking_violation_codes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>parking_violations_2025</td>
    </tr>
  </tbody>
</table>

> [!NOTE]
> Note how the new table name within our duckdb database matches the file name or the name of our DBT model which is first_model. This behaviour of DBT is essential for organizing your DBT project as each DBT model needs to be unique as it becomes a table within the database after we run it.

---

<div align="center">

<h2>✦ Thank You For Reading This Guide ✦</h2>

> *May your pipelines never break and your queries always run fast.* 🚀

</div>