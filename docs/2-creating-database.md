# Preparing Our Database

We now have all our packages installed for our project, and now we have to create our database. For this project we are going to be using DuckDB, which is relatively a new database but its perfect for this projetc as it is lightweight, and we can use it in our browser.

> [!IMPORTANT]
> The exact choice of database for projects typically depends on your company and what you need.

### 1. Create a new jupyter notebook (run-queries.ipynb) file.

- We will be using this notebook file to run our SQL queries.

```text
.
├── data
├── docs
├── .git
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── run-queries.ipynb  <------------ # Your New Notebook File Here
├── sample.py
└── screenshots
```

> [!NOTE]
> DuckDB provides a Python integration, which allows you through python or jupyter notebook to run your SQL queries, create your tables and various things you would do with a typical SQL intepreter.


- Copy paste and run the below block of codes cell by cell, in your newly created notebook file.

    - `Cell 1:` Import Necessary Dependencies.

    ```python
    import duckdb as ddb
    import pandas as pd
    ```

    - `Cell 2:` Create your first database.

    ```python
    sql_query = '''
    show tables; 
    '''

    with ddb.connect('data/nyc_parking_violations.db') as con:
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
    </tbody>
    </table>

    *In DuckDB, you can simply create a database by running a query. If the database doesn't exist it will automatically create that database.*

> [!NOTE]
> Note that we haven't created any tables as we just recently created this database, which is why it is not showing any names when we executed the above query.

### 2. Import CSV data into your database.

- Copy paste and run the below block of codes cell by cell, in your previously created notebook file.

    - `Cell 3:` SQL query to create table for violation codes (metadata).

    ```python
    sql_query_import_1 = '''
    CREATE OR REPLACE TABLE parking_violation_codes AS
    SELECT * 
    FROM read_csv_auto(
        'data/DOF_Parking_Violation_Codes_20260603.csv',
        normalize_names=True
    )
    '''
    ```
    
    - `Cell 4:` SQL query to create table for parking violation records.

    ```python
    sql_query_import_2 = '''
    CREATE OR REPLACE TABLE parking_violations_2025 AS
    SELECT * 
    FROM read_csv_auto(
        'data/sample_parking_violations_2025.csv',
        normalize_names=True
    )
    '''
    ```

    - `Cell 5:` Run the above individual SQL queries using the with statement.

    ```python
    with ddb.connect('data/nyc_parking_violations.db') as con:
        con.sql(sql_query_import_1)
        con.sql(sql_query_import_2)
    ```

> [!NOTE]
> Keep in mind that there are multiple ways of running queries using DuckDB, but using the with statement is recommended most of the time as it automatically closes the database after executing the queries. This automatic closing helps out a lot for preojects like this.

- Run the Cell 2 again to check whether the new tables has been sucessfully created or not.

```python
sql_query = '''
show tables; 
'''

with ddb.connect('data/nyc_parking_violations.db') as con:
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
      <td>parking_violation_codes</td>
    </tr>
    <tr>
      <th>1</th>
      <td>parking_violations_2025</td>
    </tr>
  </tbody>
</table>

*If you see something similar to the above result, then we have successfully created our tables into our database*


- `Cell 6:` Run a simple SELECT statement to see what our data looks like.

```python
sql_query = '''
SELECT * FROM parking_violation_codes
LIMIT 5;
'''

with ddb.connect('data/nyc_parking_violations.db') as con:
    display(con.sql(sql_query).df())
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>code</th>
      <th>definition</th>
      <th>manhattan_96th_st_below</th>
      <th>all_other_areas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>FAILURE TO DISPLAY BUS PERMIT</td>
      <td>515</td>
      <td>515</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>NO OPERATOR NAM/ADD/PH DISPLAY</td>
      <td>515</td>
      <td>515</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>UNAUTHORIZED PASSENGER PICK-UP</td>
      <td>515</td>
      <td>515</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>BUS PARKING IN LOWER MANHATTAN</td>
      <td>115</td>
      <td>115</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>BUS LANE VIOLATION</td>
      <td>250</td>
      <td>250</td>
    </tr>
  </tbody>
</table>

## Final Project Setup

```text
.
├── data
│   ├── DOF_Parking_Violation_Codes_20260603.csv
│   ├── nyc_parking_violations.db  <-------------------------------------- # Your Newly Created Database
│   ├── Parking_Violations_Issued_-_Fiscal_Year_2025_20260603.csv
│   └── sample_parking_violations_2025.csv
├── docs
│   ├── 1-coding-environment-setup.md
│   └── 2-creating-database.md
├── .git
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── run-queries.ipynb  <-------------------------------------------------- # Your New Notebook File Here
├── sample.py
├── screenshots
│   └── project-medallion-architeture.png
└── venv
```

*CONGRATULATIONS! You have sucessfully loaded the data into our project database, which we are gonna be working with throughout this project.*

---

<div align="center">

<h2>✦ Thank You For Reading This Guide ✦</h2>

> *May your pipelines never break and your queries always run fast.* 🚀

</div>