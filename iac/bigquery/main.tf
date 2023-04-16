resource "google_bigquery_dataset" "greenery" {
  dataset_id          = var.dataset_id
  friendly_name       = var.dataset_id
  description         = "This Greenery dataset"
  location            = "asia-southeast1"
  project             = var.project_id
}

resource "google_bigquery_table" "addresses" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "addresses"
  schema              = file("tables/addresses.json")
  deletion_protection = false
}

resource "google_bigquery_table" "events" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "events"
  schema              = file("tables/events.json")
  deletion_protection = false

  time_partitioning {
    expiration_ms            = null
    field                    = "created_at"
    require_partition_filter = false
    type                     = "DAY"
  }
}

resource "google_bigquery_table" "order_items" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "order_items"
  schema              = file("tables/order_items.json")
  deletion_protection = false
}

resource "google_bigquery_table" "orders" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "orders"
  schema              = file("tables/orders.json")
  deletion_protection = false

  time_partitioning {
    expiration_ms            = null
    field                    = "created_at"
    require_partition_filter = false
    type                     = "DAY"
  }
}

resource "google_bigquery_table" "products" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "products"
  schema              = file("tables/products.json")
  deletion_protection = false
}

resource "google_bigquery_table" "promos" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "promos"
  schema              = file("tables/promos.json")
  deletion_protection = false
}

resource "google_bigquery_table" "users" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.greenery.dataset_id
  table_id            = "users"
  schema              = file("tables/users.json")
  clustering          = ["first_name", "email"]
  deletion_protection = false
}
