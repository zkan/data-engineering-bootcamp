import google.auth
import pyarrow as pa
from google.auth.transport.requests import Request
from pyiceberg import catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType


REGISTRY_DATABASE_URI = "sqlite:///catalog/catalog_gcs.db"  # Replace this with your database URI
GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID" # Replace with your GCP project ID
GCS_BUCKET = "YOUR_GCS_BUCKET" # Replace with your GCS bucket
KEYFILE = "YOUR_KEYFILE_PATH" # # Replace this with your keyfile


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


# กำหนด Scope และใช้ Keyfile เพื่อยืนยันตัวตน
scopes = ["https://www.googleapis.com/auth/cloud-platform"]
access_token = get_access_token(KEYFILE, scopes)
# print(access_token.token)
# print(access_token.expiry)

# โหลด Catalog สำหรับ Iceberg และนำเอา Access Token ที่ได้มากำหนด
iceberg_catalog = catalog.load_catalog(
    "default",
    **{
        "uri": REGISTRY_DATABASE_URI,
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "gcs.oauth2.token-expires-at": access_token.expiry.timestamp(),
        "gcs.project-id": GCP_PROJECT_ID,
        "gcs.oauth2.token": access_token.token,
        "gcs.default-bucket-location": f"gs://{GCS_BUCKET}",
        "warehouse": f"gs://{GCS_BUCKET}",
    }
)

# สร้าง Namesapce หรือ Database ที่ชื่อ default
iceberg_catalog.create_namespace_if_not_exists("default")  # Replace this with your namespace

# Define the schema for the book table
schema = Schema(
    NestedField(field_id=1, name="title", field_type=StringType(), required=True),
    identifier_field_ids=[1],
)

# iceberg_catalog.drop_table("default.books") # Replace this with your table
iceberg_table = iceberg_catalog.create_table_if_not_exists(
    "default.books",    # Replace this with your table
    schema=schema,
)

# สร้างข้อมูลตารางที่มี Column ชื่อ Title
pa_table_data = pa.Table.from_pylist(
    [
        {"title": "The Lord of the Rings"},
        {"title": "Pride and Prejudice"},
        {"title": "Moby Dick"},
    ],
    schema=iceberg_table.schema().as_arrow(),
)

# iceberg_table.append(df=pa_table_data)
iceberg_table.upsert(df=pa_table_data)

print(iceberg_table.scan().to_arrow().to_string(preview_cols=10))
