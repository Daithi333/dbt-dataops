# DBT Dataops
Project for working on various datasets with DBT. Each dataset is an individual dbt project from its own sub-directory.

## Usage

### Create a new dbt project
 - Use `cd dbt_projects && dbt init` from the project root, and then fill in the project details, 
using a unique project name which does not already exist in the `dbt_projects` directory.
 - navigate to the newly created dbt project and verify it was set up correctly with `cd <my_project> && dbt debug`
 - Put the project raw data into a subdirectory of `datasets` with the same name as the project, e.g. `datasets/<my_project>`

### Load project source data into postgres
 - Add configuration for the project into `config.yml`, mirroring existing example.
 - Run `cd scripts && python load_data.py --project <my_project>` to load the source data into postgres
