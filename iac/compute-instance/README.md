# Compute Instance

## Setting up

1. Set up GCP authentication. [how to create service account](../how-to-create-service-account.md)

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

## Cleanup

To clean up the resources created by the Terraform code, run the following command:

```sh
terraform destroy
```

This will delete dataset and tables, along with all associated resources.
