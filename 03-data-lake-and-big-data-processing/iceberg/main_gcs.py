import google.auth
from google.auth.transport.requests import Request
from pyiceberg import catalog


def get_access_token(service_account_file, scopes):
    """
    Retrieves an access token from Google Cloud Platform using service account credentials.

    Args:
        service_account_file: Path to the service account JSON key file.
        scopes: List of OAuth scopes required for your application.

    Returns:
        The access token as a string.
    """

    credentials, name = google.auth.load_credentials_from_file(
        service_account_file, scopes=scopes)

    request = Request()
    credentials.refresh(request)  # Forces token refresh if needed
    return credentials


service_account_file = "dataengineercafe-61ef403fcaf4.json"
scopes = ["https://www.googleapis.com/auth/cloud-platform"]

access_token = get_access_token(service_account_file, scopes)
# print(access_token.token, access_token.expiry)

REGISTRY_DATABASE_URI = "sqlite:///catalog/catalog.db" # replace this with your database URI


catalog_inst = catalog.load_catalog(
    "default",
    **{
        "uri": REGISTRY_DATABASE_URI,
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "gcs.oauth2.token-expires-at": access_token.expiry.timestamp(),
        "gcs.project-id": "dataengineercafe", # replace with your gcp project id
        "gcs.oauth2.token": access_token.token,
        "gcs.default-bucket-location": "gs://iceberg-tmp-zkan-123", # replace with your gcs bucket
        "warehouse": "gs://iceberg-tmp-zkan-123" # replace with your gcs bucket
    }
)

import pyarrow as pa

catalog_inst.create_namespace_if_not_exists("default") # Replace this with your namespace

# Define the schema for the book table
schema = pa.schema([
    ("title", pa.string())
])

# catalog_inst.drop_table("default.books") # Replace this with your table
table = catalog_inst.create_table_if_not_exists("default.books", schema=schema)

# Create some sample data
titles = ["The Lord of the Rings", "Pride and Prejudice", "Moby Dick"]

# Create Arrow arrays from the data
title_array = pa.array(titles, type=pa.string())
table_data = pa.Table.from_arrays([title_array], names=schema.names)

table.append(table_data)
