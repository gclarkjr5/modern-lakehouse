# Modern Lakehouse

Creating a lakehouse architecture step-by-step using the same tools that ngods used. Goal is to turn this into a tutorial for training and walking through. Then also rust-ifying it :-).

## Getting Data Using yfinance

1. virtual env
2. pip install yfinance
3. create function to get data
4. create function to save data (create file if not exist, if exists, append to file)

## Using Dagster to operationalize

1. in venv, pip install dagster, dagit
2. use asset decorator with one function, then two -> materialize them
3. switch to op and job decorators
   - job is a series of ops
4. Run on a schedule
   - add a basic schedule to the existing jobs.py
   - create a workspace.yaml at the root, pointing to the dagster repo

      ```yaml
      load_from:
       - python_package: stocks
      ```

   - set DAGSTER_HOME environment variable to the root (where workspace.yaml is)
   - create a repository.py file in our dagster repo to create a dagster repository that stores and outputs all jobs, assets, schedules etc.
   - re-run dagit command
   - run `dagster-daemon run` in another terminal, make sure DAGSTER_HOME is set

## A place to store data - Minio

- staging
- bronze
- silver
- gold
