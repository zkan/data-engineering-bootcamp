# Getting Started with Analytics Engineering

## Files/Folders and What They Do

| Name | Description |
| - | - |
| `.devcontainer/devcontainer.json` | A file that tells VS Code how to access (or create) a development container with a well-defined tool and runtime stack |
| `csv_files/` | A folder that contains CSV files used for testing `dbt seed` |
| `setup/` | A folder that contains data and scripts used for initializing the Postgres database used in this project |
| `yaml_files/` | A folder that contains the YAML file examples such as `profiles.yml` or `src.yml` |
| `.gitignore` | A file that specifies intentionally untracked files that Git should ignore |
| `LICENSE` | A license of this repo |
| `Makefile` | A Makefile file which defines set of tasks to be executed |
| `README.md` | README file that provides the setup instruction on this project |
| `docker-compose.yml` | A Docker Compose file that runs a Postgres database and SQLPad used in this project |
| `greenery-dbdiagram.txt` | A file that provides code for drawing an ER diagram on [dbdiagram.io](https://dbdiagram.io/home) |
| `requirements.txt` | A file that contains Python package dependencies for this code repository |

## Getting Started

To start the Docker compose:

```sh
make up
```

### To Set Up and Activate Your Python Virtual Environment

```bash
python -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
```

### To Initialize A dbt Project

```bash
dbt init
```

**Note:** Let's specify the project name `greenery`.

### To Set Up Your dbt Profile

1. Change the directory to your dbt project.

    ```bash
    cd <dbt_project_name>
    ```

1. Run the following command to copy the profiles example file to the real
   profiles file in the project folder.

    ```bash
    cp ../yaml_files/profiles.yml .
    ```

1. Edit the content in the `profiles.yml` file by changing the output and
   target to your name (e.g., `dbt_john`), and save. See the example below.

    ```yaml
    greenery:

      outputs:
        dbt_zkan:
          type: postgres
          threads: 1
          host: localhost
          port: 5432
          user: postgres
          pass: "{{ env_var('DBT_ENV_SECRET_PG_PASSWORD') }}"
          dbname: greenery
          schema: dbt_zkan

        prod:
          type: postgres
          threads: 1
          host: localhost
          port: 5432
          user: postgres
          pass: "{{ env_var('DBT_ENV_SECRET_PG_PASSWORD') }}"
          dbname: greenery
          schema: prod

      target: dbt_zkan
    ```

1. Set the environment variable.

    ```bash
    export DBT_ENV_SECRET_PG_PASSWORD=postgres
    ```

1. We then should be able to use dbt now. :-)

### To Debug The dbt Project

```bash
export DBT_ENV_SECRET_PG_PASSWORD=postgres
cd <dbt_project_name>
dbt debug
```

### To Create Your Data Models

```bash
export DBT_ENV_SECRET_PG_PASSWORD=postgres
cd <dbt_project_name>
dbt run
```

### To Test Your Data Models

```bash
export DBT_ENV_SECRET_PG_PASSWORD=postgres
cd <dbt_project_name>
dbt test
```

### To Generate The dbt Documentation and Serve It

```bash
export DBT_ENV_SECRET_PG_PASSWORD=postgres
cd <dbt_project_name>
dbt docs generate
dbt docs serve
```
