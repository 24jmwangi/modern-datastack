variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "modern-datastack"
}

variable "region" {
  description = "The region where resources will be created"
  type        = string
  default     = "us-central1"
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

variable "project_id" {
  type = string
}

variable "region" {
  type = string
}