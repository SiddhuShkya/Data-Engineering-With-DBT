# Preparing Our DBT Environment

We are now ready to create our dbt project and prepare our dbt project environment. 

### 1. Create a new dbt project.

Creating a project with dbt is very simple as it has a built-in command called dbt init, which will auto-generate a new DBT Project with every file you need to get started, as well as the DBTs directory properly oraganized for you. 

- Use the below command to initialize a new dbt project.

```sh
$ dbt init
```

- You might get something like the below prompt, which is asking for the name of your project. Type in the below given project name and hit enter.

> Project Name: nyc_parking_violations

```sh
(venv) siddhu@ubuntu:~/Desktop/Data-Engineering-With-DBT$ dbt init
05:25:32  Running with dbt=1.8.9
05:25:32  [ConfigFolderDirectory]: Unable to parse logging event dictionary. Failed to parse dir field: expected string or bytes-like object, got 'PosixPath'.. Dictionary: {'dir': PosixPath('/home/siddhu/.dbt')}
05:25:32  Creating dbt configuration folder at 
Enter a name for your project (letters, digits, underscore): 
```

- Again, you might get a prompt similar to below one, asking for what database connection we want to use. Since, we are using duckdb connection type in 1 to signify that and hit enter.

```text
05:28:06  Setting up your profile.
Which database would you like to use?
[1] duckdb

(Don't see the one you want? https://docs.getdbt.com/docs/available-adapters)

Enter a number: 
```

- You should be able to see the final result similar to the below one indicating that your new dbt project has successfully been created.

```sh
05:30:36  Profile nyc_parking_violations written to /home/siddhu/.dbt/profiles.yml using target's sample configuration. Once updated, you'll be able to start developing with dbt.
```

- You should also be able to see 2 new folders named logs and nyc_parking_violations in your current project directory.

```text
.
├── data
├── docs
├── .git
├── .gitignore
├── LICENSE
├── logs  <-------------------------------- # Your Newly Generated DBT Project Folder
├── nyc_parking_violations <--------------- # Your Newly Generated DBT Project Folder
├── README.md
├── requirements.txt
├── run-queries.ipynb
├── sample.py
├── screenshots
└── venv
```

### 2. Prepare your dbt environment.

The dbt init has auto-generated some files which are important for building our project. The below tree structure shows all the new important files that were previously generated which are inside the new folders logs and nyc_parking_violations

```text
.
├── data
├── docs
├── .git
├── .gitignore
├── LICENSE
├── logs
│   └── dbt.log
├── nyc_parking_violations
│   ├── analyses
│   ├── dbt_project.yml
│   ├── .gitignore
│   ├── macros
│   ├── models
│   ├── README.md
│   ├── seeds
│   ├── snapshots
│   └── tests
├── README.md
├── requirements.txt
├── run-queries.ipynb
├── sample.py
├── screenshots
└── venv
```

- Among all the above auto-generated files, the dbt_project.yml file is the most important one. The YML stands for Yet Another Markdown Language which quickly summarizes the configuration of your any entire project.

```yml
# Name your project! Project names should contain only lowercase characters
# and underscores. A good package name should reflect your organization's
# name or the intended use of these models
name: 'nyc_parking_violations'
version: '1.0.0'

# This setting configures which "profile" dbt uses for this project.
profile: 'nyc_parking_violations'

# These configurations specify where dbt should look for different types of files.
# The `model-paths` config, for example, states that models in this project can be
# found in the "models/" directory. You probably won't need to change these!
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:         # directories to be removed by `dbt clean`
  - "target"
  - "dbt_packages"


# Configuring models
# Full documentation: https://docs.getdbt.com/docs/configuring-models

# In this example config, we tell dbt to build all models in the example/
# directory as views. These settings can be overridden in the individual model
# files using the `{{ config(...) }}` macro.
models:
  nyc_parking_violations:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: view
```

*The dbt_project.yml file has key sections which informs your DBT project, where to look for and what actions it should take, when its running your DBT project. When we start building our project we will learn more about how to set this up for our project.*

- We now need to manually create our new yaml configuration file called the profiles.yml file. 

```sh
$ cd nyc_parking_violations/
$ touch profiles.yml
```

- You should be able to see your new yaml file created inside the nyc_parking_violations directoy.

```text
.
├── analyses
├── dbt_project.yml
├── .gitignore
├── macros
├── models
├── profiles.yml  <-------------- # Your Newly Created YAML file
├── README.md
├── seeds
├── snapshots
└── tests
```

- Copy paste the below configuration to your new profiles.yml file.

```yml
default:
  target: dev
  outputs:
    dev: 
      type: duckdb
```

> Source: [Configure Your Profile For DBT DuckDB](https://github.com/duckdb/dbt-duckdb#configure-your-profile)

*We have successfully set our default profile as this target dev, where we have the type of duck db for our outputs for our database.*

- Now we are going to connect our dbt_project.yml file and profiles.yml file. If you look at dbt_project file you will see that profile has the value 'nyc_parking_violations' but in our previous profiles.yml we had default instead. So we need to update our profiles.yml file to match the dbt_project.yml file's profile.

```yml
nyc_parking_violations:
  target: dev        
  outputs:
    dev: 
      type: duckdb
```

>  [!IMPORTANT]
> This is a required step because when you run your DBT project from the command line, it reads your db_project.yml file to find the profile name and then looks for a profile with the same name in your profiles.yml file. This profiles.yml contains all the information dbt needs to connect to your data platform.

- Check your current working directory, to verify you are inside the nyc_parking_violation directory.

```sh
$ pwd
```
```sh
/home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations
```

*You should be able to see a path similar to the above one.*

- Run the dbt debig command to run our project and to see that if everything is working fine or not.

```sh
$ dbt debug
```
```sh
06:31:10  Running with dbt=1.8.9
06:31:10  dbt version: 1.8.9
06:31:10  python version: 3.11.15
06:31:10  python path: /home/siddhu/Desktop/Data-Engineering-With-DBT/venv/bin/python3.11
06:31:10  os info: Linux-6.14.0-37-generic-x86_64-with-glibc2.39
06:31:10  Using profiles dir at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations
06:31:10  Using profiles.yml file at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations/profiles.yml
06:31:10  Using dbt_project.yml file at /home/siddhu/Desktop/Data-Engineering-With-DBT/nyc_parking_violations/dbt_project.yml
06:31:10  adapter type: duckdb
06:31:10  adapter version: 1.8.4
06:31:10  Configuration:
06:31:10    profiles.yml file [OK found and valid]
06:31:10    dbt_project.yml file [OK found and valid]
06:31:10  Required dependencies:
06:31:10   - git [OK found]

06:31:10  Connection:
06:31:10    database: memory
06:31:10    schema: main
06:31:10    path: :memory:
06:31:10    config_options: None
06:31:10    extensions: None
06:31:10    settings: {}
06:31:10    external_root: .
06:31:10    use_credential_provider: None
06:31:10    attach: None
06:31:10    filesystems: None
06:31:10    remote: None
06:31:10    plugins: None
06:31:10    disable_transactions: False
06:31:10  Registered adapter: duckdb=1.8.4
06:31:10    Connection test: [OK connection ok]

06:31:10  All checks passed!
```

*If you see something similar to the above "All checks passed!", then congratulations we have successfully connected our DBT yml files to each other and the DBT can now run successfully.*

---

<div align="center">

<h2>✦ Thank You For Reading This Guide ✦</h2>

> *May your pipelines never break and your queries always run fast.* 🚀

</div>