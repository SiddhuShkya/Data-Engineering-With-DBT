# Preparing Our Coding Environment

This guide walks you through setting up a local Python development environment
for data engineering with DBT (Data Build Tool) and DuckDB. By the end, you'll
have all the necessary dependencies installed and be ready to build data
pipelines using a modern, lightweight stack.

## Current Project Setup

```text
.
├── data
│   ├── DOF_Parking_Violation_Codes_20260603.csv
│   ├── Parking_Violations_Issued_-_Fiscal_Year_2025_20260603.csv
│   └── sample_parking_violations_2025.csv
├── docs
│   └── coding-environment-setup.md
├── .git
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── sample.py
└── screenshots
    └── project-medallion-architeture.png
```

### 1. Create a python virtual environment.

- Create a python virtual environment using the below command.

```sh
$ python3.11 -m venv venv
```

- Activate the newly created environment.

```sh
$ source venv/bin/activate
```

### 2. Install the dbt core via pip

- The first thing we are going to do is download DBT, specifically DBT core. We are going to be using PIP to install packages.

```sh
(venv) $ pip install dbt-core==1.6.1 
```

- After completing the above installation, you can verify if the package has been installed or not using the below command.

```sh
(venv) $ pip show dbt-core
```
```sh
Name: dbt-core
Version: 1.6.1
Summary: With dbt, data analysts and engineers can build analytics the way engineers build applications.
Home-page: https://github.com/dbt-labs/dbt-core
Author: dbt Labs
Author-email: info@dbtlabs.com
License: 
Location: /home/siddhu/Desktop/Data-Engineering-With-DBT/venv/lib/python3.12/site-packages
Requires: agate, cffi, click, colorama, dbt-extractor, dbt-semantic-interfaces, hologram, idna, isodate, Jinja2, logbook, mashumaro, minimal-snowplow-tracker, networkx, packaging, pathspec, protobuf, pytz, pyyaml, requests, sqlparse, typing-extensions, urllib3
Required-by: 
```

*You should see an output like the above one.*


### 3. Install the dbt connector to DuckDB.

DBT Core is the foundational package and we have various connectors to different databases within the data ecosystem. For this prject we will using something known as DuckDB.

- Install DuckDB for dbt using PIP.

```sh
(venv) $ pip install dbt-duckdb==1.6.0
```

- Verify the package installation.

```sh
(venv) $ pip show dbt-duckdb
```
```sh
Name: dbt-duckdb
Version: 1.6.0
Summary: The duckdb adapter plugin for dbt (data build tool)
Home-page: https://github.com/jwills/dbt-duckdb
Author: Josh Wills
Author-email: joshwills+dbt@gmail.com
License: 
Location: /home/siddhu/Desktop/Data-Engineering-With-DBT/venv/lib/python3.12/site-packages
Requires: dbt-core, duckdb
Required-by: 
```

### 4. Install the DuckDB package via pip.

dbt-core is the connection to DBT and DuckDB is the actual database itself and using it with python.  

- Install DuckDB using PIP.

```sh
(venv) $ pip install duckdb==0.9.0
```

- Verify the package installation.

```sh
 (venv) $ pip show duckdb
```
```sh
Name: duckdb
Version: 0.9.0
Summary: DuckDB embedded database
Home-page: https://www.duckdb.org
Author: 
Author-email: 
License: MIT
Location: /home/siddhu/Desktop/Data-Engineering-With-DBT/venv/lib/python3.11/site-packages
Requires: 
Required-by: dbt-duckdb
```

### 5. Update your requirements.txt

- Copy paste the below to requirements.txt file.

```text
ipykernel
pandas
requests>=2.28 
dbt-core==1.6.1 
dbt-duckdb==1.6.0
duckdb==0.9.0
```

## Final Project Setup

```text
.
├── data
│   ├── DOF_Parking_Violation_Codes_20260603.csv
│   ├── Parking_Violations_Issued_-_Fiscal_Year_2025_20260603.csv
│   └── sample_parking_violations_2025.csv
├── docs
│   └── coding-environment-setup.md
├── .git
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── sample.py
├── screenshots
│   └── project-medallion-architeture.png
└── venv
```

---

<div align="center">

<h2>✦ Thank You For Reading This Guide ✦</h2>

> *May your pipelines never break and your queries always run fast.* 🚀

</div>