# Implementing Tests Within Your DBT Project

Now we're going to implement tests for our dbt project. There are singular tests, generic tests, and then also among the generic tests there's some out-of-the-box tests, such as unique, not_null, accepted_values, and relationships. We'll be implementing all of them for this project.

### 1. Creating custom singular tests.

- Go into your tests folder

```text
.
├── analyses
├── dbt_project.yml
├── .gitignore
├── logs
├── macros
├── models
├── profiles.yml
├── README.md
├── seeds
├── snapshots
├── target
├── tests <------------------ # Your tests folder here
│   └── .gitkeep
└── .user.yml
```

- Create a new file called violation_codes_revenue.sql inside the tests folder.

```sh
$ cd nyc_parking_violations/
$ touch tests/violation_codes_revenue.sql
```

*The test for these singular tests are just SQL files. If these SQL queries return any values, then it's going top fail this test or give a warning.*

- Copy and paste the below SQL query to the recently created sql file.

```sql
{{config(severity='warn')}}
SELECT 
    violation_code,
    SUM(fee_usd) AS total_revenue_usd
FROM
    {{ref('silver_parking_violation_codes')}}
GROUP BY
    violation_code
HAVING
    NOT (total_revenue_usd >= 1)
```

> [!NOTE]
> '{{config(severity='warn')}}' is a jinja feature called config which helps to avoid error and replaces it with an warning instead.

*Now that we have our test ready, let's try this out.*

- Run the dbt tests command.

```sh
$ dbt test
```
```sh
07:44:51  Running with dbt=1.8.9
07:44:51  Registered adapter: duckdb=1.8.4
07:44:52  Found 10 models, 3 data tests, 426 macros
07:44:52  
07:44:52  Concurrency: 1 threads (target='dev')
07:44:52  
07:44:52  1 of 3 START test not_null_bronze_parking_violations_summons_number ............ [RUN]
07:44:52  1 of 3 PASS not_null_bronze_parking_violations_summons_number .................. [PASS in 0.04s]
07:44:52  2 of 3 START test unique_bronze_parking_violations_summons_number .............. [RUN]
07:44:52  2 of 3 PASS unique_bronze_parking_violations_summons_number .................... [PASS in 0.02s]
07:44:52  3 of 3 START test violation_codes_revenue ...................................... [RUN]
07:44:52  3 of 3 WARN 1 violation_codes_revenue .......................................... [WARN 1 in 0.02s]
07:44:52  
07:44:52  Finished running 3 data tests in 0 hours 0 minutes and 0.23 seconds (0.23s).
07:44:52  
07:44:52  Completed with 1 warning:
07:44:52  
07:44:52  Warning in test violation_codes_revenue (tests/violation_codes_revenue.sql)
07:44:52  Got 1 result, configured to warn if != 0
07:44:52  
07:44:52    compiled code at target/compiled/nyc_parking_violations/tests/violation_codes_revenue.sql
07:44:52  
07:44:52  Done. PASS=2 WARN=1 ERROR=0 SKIP=0 TOTAL=3
```

*As you can see we have been given a warning because there is a value in there that didn't pass, specifically in violation_code_revenue.*

- Check the output of the above test SQL file using the run-queries.ipynb, by running the below block of code.

```python
sql_query = """
SELECT 
    violation_code,
    SUM(fee_usd) AS total_revenue_usd
FROM
    'silver_parking_violation_codes'
GROUP BY
    violation_code
HAVING
    NOT (total_revenue_usd >= 1)
"""

with ddb.connect("data/nyc_parking_violations.db") as con:
    display(con.sql(sql_query).df())
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>violation_code</th>
      <th>total_revenue_usd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>41</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>

*We can see that the violation code 41 has 0 revenue for it.*

### 2. Implementing tests within the schema.yml file