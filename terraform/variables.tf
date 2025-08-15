variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "my-data-pipeline-project"
}

variable "region" {
  description = "The region where resources will be created"
  type        = string
  default     = "us-central1"
}

variable "postgres_db_name" {
  description = "The name of the PostgreSQL database"
  type        = string
  default     = "my_database"
}

variable "postgres_user" {
  description = "The username for PostgreSQL"
  type        = string
  default     = "db_user"
}

variable "postgres_password" {
  description = "The password for PostgreSQL"
  type        = string
  sensitive   = true
}

variable "bigquery_dataset_silver" {
  description = "The name of the BigQuery dataset for silver layer"
  type        = string
  default     = "silver_dataset"
}

variable "bigquery_dataset_gold" {
  description = "The name of the BigQuery dataset for gold layer"
  type        = string
  default     = "gold_dataset"
}