## Data Engineering With DBT (Data Build Tool)

Data Build Tool (dbt) has quickly become an essential tool in many data stacks ranging from startups to big tech for managing data transformations. In this course, data engineer Mark Freeman helps you get started with setting up, running, and managing a dbt project via the open-source offering dbt Core. Learn how to install dbt Core, configure an environment for dbt, create and manage a dbt project, and deploy a dbt project in production. If you’re a data professional tasked with implementing dbt within your organization, recently joined a team utilizing dbt and need to upskill, or just want to learn about dbt to increase your competitiveness within the data job market, check out this course.

### Course Learning Outcomes

---

The below are some of the main learning outcomes for this course:

- Setting up an dbt project.
- Set up a database.
- Connect your dbt project to that database.
- Set up your own data workflows using dbt using real world data. 


### Project Scenario

---

In this project, I am an data engineer who has been given a task to transform the raw new york city parking violation data into the medallion architecture for the company's data lakehouse. My team has decided to use dbt core to implement this project as it allows us to use the best of software engineering practices for the SQL transformation. 

### Project Architetcure

---

<img src="./screenshots/project-medallion-architeture.png"
    alt="Image Caption"
    style="border:1px solid white; padding:1px; background:#fff; width: 3000px;" />

> The above diagram shows the medallion architecture for this project which is broken down into 3 different parts: 

- `🥉 Bronze`: This part typically has the raw data that we bring into our analytical database.
- `🥈 Silver`: This is the raw data transformed into a data model of our desire.
- `🥇 Gold`: Metrics data built on top of data model. 

### Project Datasets

---

The dataset that we will be using for this project is the New York City parking violations issued for fiscal year 2025 and the New York City Department of Finance (DOF) violation codes, which is essentially the metadata about the violations. 

- Original Dataset Link: [Parking Violations Issued - Fiscal Year 2025](https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2025/m5vz-tzqv/about_data)

- Violation Codes Dataset Link: [DOF Parking Violation Codes](https://data.cityofnewyork.us/Transportation/DOF-Parking-Violation-Codes/ncbg-6agr/about_data)

This data is sourced from NYC Open Data, which is government dataset that's public for anyone to use. In our case we will be using the sampled version of this dataaset for our personal project.

> [!NOTE]
> This above dataset for parking violations is massive, around millions of rows. However for this project we will only be dealing with a small sample as it would much easier to work with. 








