# DBT Dataops
Project for working on various datasets with DBT. Each dataset is an individual dbt project from its own sub-directory.

## Usage

### Create a new dbt project
 - Use `cd dbt_projects && dbt init` from the project root, and then fill in the project details, 
using a unique project name which does not already exist in the `dbt_projects` directory.
 - navigate to the newly created dbt project and verify it was set up correctly with `cd <my_project> && dbt debug`
 - Put the project raw data into a subdirectory of `datasets` with the same name as the project, e.g. `datasets/<my_project>`

### Load project source data into postgres
 - Add configuration for the dbt project into `config.yml` mirroring the example below. If the source data is 
missing headers, then column definitions needs to be defined. Otherwise, it can be left empty, and the loader (pandas)
will decide the column names and types based on the data. (This will suffice for now, but will likely need to move to 
a fully declarative table definition, creation and data loaded separately afterwards.)
   ```
     addresses:
        schema: addresses
        description: Reference data for cities and addresses
        tables:
          cities:
            source: cities.csv
            columns:
              - name: city
                type: text
          addresses:
            source: addresses.csv
   ```
 - Run `cd scripts && python load_data.py --project <my_project>` to load the source data into postgres

### Install dbt deps in project
To install a dbt dependency, for example a [testing dependency](https://hub.getdbt.com/metaplane/dbt_expectations/latest/) 
for asserting data types:

1. add or update the `package.yml` in the dbt project root 
    ```
    packages:
      - package: metaplane/dbt_expectations
        version: 0.10.9
    ```
2. Run `dbt deps` to install
