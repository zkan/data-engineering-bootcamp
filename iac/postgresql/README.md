# PostgreSQL

This Terraform project sets up a PostgreSQL database instance on Google Cloud SQL along with a database.

## Setting up

1. Set up GCP authentication.

    - Navigate to the GCP Console and select **IAM & Admin** > **Service accounts**.
    - Click **Create Service Account** and provide a name for the account.
    - Select the **Cloud SQL Admin** role.
    - Click **Create**.
    - Select the newly created service account and click **Create Key**.
    - Choose JSON as the key type and click **Create**.
    - Save the JSON file in a secure location.

1. Export the Service Account JSON file.

    ```sh
    export GOOGLE_CREDENTIALS=<YOUR_SERVICE_ACCOUNT_JSON_FILE_PATH>
    ```

1. Initialize Terraform.

    ```sh
    terraform init
    ```

1. Apply the Terraform code to create the SQL instance and database.

    ```sh
    terraform apply
    ```

    When prompted by Terraform, enter the following values:

    - `project` The ID of the Google Cloud Platform project you want to use.
    - `root_password` The password for the PostgreSQL root user.

1. Once the Terraform code has been applied, run the `initialize-data` script to initialize the master data.

    ```sh
    sh initialize-data
    ```

    The script will prompt you to enter the password for the PostgreSQL user `postgres`. After entering the password, the script will initialize the master data into the `greenery` database in the SQL instance.

## Cleanup

To clean up the resources created by the Terraform code, run the following command:

```sh
terraform destroy
```

This will delete the SQL instance and database, along with all associated resources.
