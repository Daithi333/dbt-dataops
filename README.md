# DBT Dataops
Project for working on various datasets with DBT. Each dataset is an individual dbt project from its own subdirectory.

## Overview
 - A 'minimal intervention' approach has been adopted for the loading of source data into postgres. A basic definition 
of the project should be defined in the `source_config.yml` and columns need to be defined for any data which does 
not have headers. An example of a project with 2 sources is below, one which has no headers, so columns arte defined.
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
- Mixed or upper case headers cause problems with DBT test definitions, as postgres folds unquoted identifiers into 
lower case. While this could be handled in the initial data load with declarative table definitions, it is data 
transformation and is contrary to the 'minimum intervention' approach, so this is handled by the bronze models. 

## Usage

### First time only
 - Create a `.env` at the project root mirroring the `.env.example`, and populate the variables.

### Create a new dbt project
 - Use `cd dbt_projects && dbt init` from the project root, and then fill in the project details, 
using a unique project name which does not already exist in the `dbt_projects` directory.
 - navigate to the newly created dbt project and verify it was set up correctly with `cd <my_project> && dbt debug`
 - Put the project raw data into a subdirectory of `datasets` with the same name as the project, e.g. `datasets/<my_project>`

### Load project source data into postgres
 - Add configuration for the dbt project into `source_config.yml` mirroring the example in the overview.
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

### TODOS
 - 
 - Mixed and upper case column names cause issues with dbt / postgres
