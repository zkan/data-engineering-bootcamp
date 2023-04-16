variable "database_version" {
  description = "The database server version."
  type        = string
  default     = "POSTGRES_14"
}

variable "name" {
  description = "The name of the database instance."
  type        = string
  default     = "greenery"
}

variable "project" {
  description = "The ID of the GCP project to manage resources in."
  type        = string
}

variable "region" {
  description = "The region name of geographic location. See https://cloud.google.com/bigquery/docs/dataset-locations."
  type        = string
  default     = "asia-southeast1"
}

variable "root_password" {
  description = "The password for `root` user."
  type        = string
}

variable "tier" {
  description = "The machine type to use. See https://cloud.google.com/sql/docs/admin-api/v1beta4/tiers."
  type        = string
  default     = "db-f1-micro"
}
