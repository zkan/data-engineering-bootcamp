resource "google_sql_database_instance" "this" {
  name                = var.name
  database_version    = var.database_version
  deletion_protection = false
  project             = var.project
  region              = var.region
  root_password       = var.root_password

  settings {
    tier = var.tier
    ip_configuration {
      authorized_networks {
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_database" "this" {
  name     = var.name
  instance = google_sql_database_instance.this.name
  project  = var.project
}
