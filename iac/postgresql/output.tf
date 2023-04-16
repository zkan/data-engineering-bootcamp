output "public_ip_address" {
  description = "The public IPv4 address assigned."
  value = google_sql_database_instance.this.public_ip_address
}
