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

In addition to the singular custom tests, we can also implement tests via the schema.yml file.

- Go into your schema.yml file and use the generic tests that are prebuilt in dbt that are out of the box.

```text
.
├── analyses
├── dbt_project.yml
├── .gitignore
├── logs
├── macros
├── models
│   ├── bronze
│   ├── docs
│   │   ├── docs_block.md
│   │   └── schema.yml  <--------------- # Your schema.yml file here
│   ├── example
│   ├── gold
│   └── silver
├── profiles.yml
├── README.md
├── seeds
├── snapshots
├── target
├── tests
└── .user.yml
```

- Inside schema.yml, go into bronze_parking_violation and for summons_number and add some tests.

```yml
- name: bronze_parking_violations 
    description: Raw data related to parking violations in 2023, encompassing various details about each violation.
    columns:
      - name: summons_number
        description: '{{ doc("summons_number") }}'
        data_tests:       
          - unique
          - not_null
```
*We added the tests field below the description with values unique and not null.*

- Run dbt test to check if everythings working fine or not.

```sh
$ dbt test
```
```sh
14:27:36  Running with dbt=1.8.9
14:27:37  Registered adapter: duckdb=1.8.4
14:27:37  [WARNING]: Deprecated functionality
The `tests` config has been renamed to `data_tests`. Please see
https://docs.getdbt.com/docs/build/data-tests#new-data_tests-syntax for more
information.
14:27:37  Found 10 models, 3 data tests, 426 macros
14:27:37  
14:27:37  Concurrency: 1 threads (target='dev')
14:27:37  
14:27:37  1 of 6 START sql view model main.bronze_parking_violation_codes ................ [RUN]
14:27:37  1 of 6 OK created sql view model main.bronze_parking_violation_codes ........... [OK in 0.08s]
14:27:37  2 of 6 START sql view model main.bronze_parking_violations ..................... [RUN]
14:27:38  2 of 6 OK created sql view model main.bronze_parking_violations ................ [OK in 0.07s]
14:27:38  3 of 6 START sql view model main.silver_violation_tickets ...................... [RUN]
14:27:38  3 of 6 OK created sql view model main.silver_violation_tickets ................. [OK in 0.04s]
14:27:38  4 of 6 START sql view model main.silver_violation_vehicles ..................... [RUN]
14:27:38  4 of 6 OK created sql view model main.silver_violation_vehicles ................ [OK in 0.04s]
14:27:38  5 of 6 START sql table model main.gold_ticket_metrics .......................... [RUN]
14:27:38  5 of 6 OK created sql table model main.gold_ticket_metrics ..................... [OK in 0.06s]
14:27:38  6 of 6 START sql table model main.gold_vehicle_metrics ......................... [RUN]
14:27:38  6 of 6 OK created sql table model main.gold_vehicle_metrics .................... [OK in 0.05s]
14:27:38  
14:27:38  Finished running 4 view models, 2 table models in 0 hours 0 minutes and 0.51 seconds (0.51s).
14:27:38  
14:27:38  Completed successfully
14:27:38  
14:27:38  Done. PASS=6 WARN=0 ERROR=0 SKIP=0 TOTAL=6
(venv) siddhu@ubuntu:~/Desktop/Data-Engineering-With-DBT/nyc_parking_violations$ dbt test
14:27:54  Running with dbt=1.8.9
14:27:54  Registered adapter: duckdb=1.8.4
14:27:54  Found 10 models, 3 data tests, 426 macros
14:27:54  
14:27:54  Concurrency: 1 threads (target='dev')
14:27:54  
14:27:54  1 of 3 START test not_null_bronze_parking_violations_summons_number ............ [RUN]
14:27:54  1 of 3 PASS not_null_bronze_parking_violations_summons_number .................. [PASS in 0.04s]
14:27:54  2 of 3 START test unique_bronze_parking_violations_summons_number .............. [RUN]
14:27:54  2 of 3 PASS unique_bronze_parking_violations_summons_number .................... [PASS in 0.02s]
14:27:54  3 of 3 START test violation_codes_revenue ...................................... [RUN]
14:27:54  3 of 3 WARN 1 violation_codes_revenue .......................................... [WARN 1 in 0.02s]
14:27:54  
14:27:54  Finished running 3 data tests in 0 hours 0 minutes and 0.19 seconds (0.19s).
14:27:55  
14:27:55  Completed with 1 warning:
14:27:55  
14:27:55  Warning in test violation_codes_revenue (tests/violation_codes_revenue.sql)
14:27:55  Got 1 result, configured to warn if != 0
14:27:55  
14:27:55    compiled code at target/compiled/nyc_parking_violations/tests/violation_codes_revenue.sql
14:27:55  
14:27:55  Done. PASS=2 WARN=1 ERROR=0 SKIP=0 TOTAL=3
```

*You can also see the additional test we recently added.*

- You can also create you own generic test by creating a generic folder inside the tests folder.

```sh
$ mkdir tests/generic
```

- Create a new file called generic_not_null.sql inside the newly created generic folder.

```sh
$ touch tests/generic/generic_not_null.sql
```

- In this generic sql test file we will be using a jinja test function. Copy paste the below jinja function to the generic_not_null.sql file

```sql
{% test generic_not_null(model, column_name) %}

    SELECT * 
    FROM {{ model }}
    WHERE {{ column_name }} IS NULL

{% endtest %}
```

- Go back to your schema.yml file and add this test.

```yml
- name: bronze_parking_violations 
    description: Raw data related to parking violations in 2023, encompassing various details about each violation.
    columns:
      - name: summons_number
        description: '{{ doc("summons_number") }}'
        data_tests:       
          - unique
          - not_null
          - generic_not_null
```

- Run dbt test again to check if everythings working fine or not.

```sh
$ dbt test
```
```sh
14:41:43  Running with dbt=1.8.9
14:41:43  Registered adapter: duckdb=1.8.4
14:41:44  [WARNING]: Deprecated functionality
The `tests` config has been renamed to `data_tests`. Please see
https://docs.getdbt.com/docs/build/data-tests#new-data_tests-syntax for more
information.
14:41:44  Found 10 models, 4 data tests, 427 macros
14:41:44  
14:41:44  Concurrency: 1 threads (target='dev')
14:41:44  
14:41:44  1 of 4 START test generic_not_null_bronze_parking_violations_summons_number .... [RUN]
14:41:44  1 of 4 PASS generic_not_null_bronze_parking_violations_summons_number .......... [PASS in 0.04s]
14:41:44  2 of 4 START test not_null_bronze_parking_violations_summons_number ............ [RUN]
14:41:44  2 of 4 PASS not_null_bronze_parking_violations_summons_number .................. [PASS in 0.02s]
14:41:44  3 of 4 START test unique_bronze_parking_violations_summons_number .............. [RUN]
14:41:44  3 of 4 PASS unique_bronze_parking_violations_summons_number .................... [PASS in 0.02s]
14:41:44  4 of 4 START test violation_codes_revenue ...................................... [RUN]
14:41:44  4 of 4 WARN 1 violation_codes_revenue .......................................... [WARN 1 in 0.02s]
14:41:44  
14:41:44  Finished running 4 data tests in 0 hours 0 minutes and 0.20 seconds (0.20s).
14:41:44  
14:41:44  Completed with 1 warning:
14:41:44  
14:41:44  Warning in test violation_codes_revenue (tests/violation_codes_revenue.sql)
14:41:44  Got 1 result, configured to warn if != 0
14:41:44  
14:41:44    compiled code at target/compiled/nyc_parking_violations/tests/violation_codes_revenue.sql
14:41:44  
14:41:44  Done. PASS=3 WARN=1 ERROR=0 SKIP=0 TOTAL=4
```

*We see our generic_not_null test happening.*

- You can also make it so that you can see the results of your test using the dbt_project.yml, simply add the below value at the end.

```yml
tests:
  +store_failures: true
```

- Run dbt test again.

```sh
$ dbt test
```
```sh
The `tests` config has been renamed to `data_tests`. Please see
https://docs.getdbt.com/docs/build/data-tests#new-data_tests-syntax for more
information.
14:46:24  Registered adapter: duckdb=1.8.4
14:46:24  Found 10 models, 4 data tests, 427 macros
14:46:24  
14:46:24  Concurrency: 1 threads (target='dev')
14:46:24  
14:46:24  1 of 4 START test generic_not_null_bronze_parking_violations_summons_number .... [RUN]
14:46:25  1 of 4 PASS generic_not_null_bronze_parking_violations_summons_number .......... [PASS in 0.07s]
14:46:25  2 of 4 START test not_null_bronze_parking_violations_summons_number ............ [RUN]
14:46:25  2 of 4 PASS not_null_bronze_parking_violations_summons_number .................. [PASS in 0.04s]
14:46:25  3 of 4 START test unique_bronze_parking_violations_summons_number .............. [RUN]
14:46:25  3 of 4 PASS unique_bronze_parking_violations_summons_number .................... [PASS in 0.04s]
14:46:25  4 of 4 START test violation_codes_revenue ...................................... [RUN]
14:46:25  4 of 4 WARN 1 violation_codes_revenue .......................................... [WARN 1 in 0.04s]
14:46:25  
14:46:25  Finished running 4 data tests in 0 hours 0 minutes and 0.37 seconds (0.37s).
14:46:25  
14:46:25  Completed with 1 warning:
14:46:25  
14:46:25  Warning in test violation_codes_revenue (tests/violation_codes_revenue.sql)
14:46:25  Got 1 result, configured to warn if != 0
14:46:25  
14:46:25    compiled code at target/compiled/nyc_parking_violations/tests/violation_codes_revenue.sql
14:46:25  
14:46:25    See test failures:
  ---------------------------------------------------------------------------------------
  select * from "nyc_parking_violations"."main_dbt_test__audit"."violation_codes_revenue"
  ---------------------------------------------------------------------------------------
14:46:25  
14:46:25  Done. PASS=3 WARN=1 ERROR=0 SKIP=0 TOTAL=4
```

*We can see our test failures over here.*

- Copy the test failure and run the same query using the run-queries.ipynb file.

```python
sql_query = """
select * from "nyc_parking_violations"."main_dbt_test__audit"."violation_codes_revenue"
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

*This is how you run tests in dbt.*

We have finally completed our DBT project, we have all our models running, we have documentation, and we have tests, and the final step with our complete dbt project is to put it into production.

---

<div align="center">

<h2>✦ Thank You For Reading This Guide ✦</h2>

> *May your pipelines never break and your queries always run fast.* 🚀

</div>