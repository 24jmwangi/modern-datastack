output "postgresql_connection_string" {
  value = "postgresql://${var.db_username}:${var.db_password}@${var.db_host}:${var.db_port}/${var.db_name}"
}

output "bigquery_dataset_id" {
  value = var.bigquery_dataset_id
}

output "silver_dataset_id" {
  value = var.silver_dataset_id
}

output "gold_dataset_id" {
  value = var.gold_dataset_id
}