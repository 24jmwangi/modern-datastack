variable "region" {
  description = "The region where resources will be created"
  type        = string
  default     = "US"
}


variable "bigquery_dataset_silver2" {
  description = "The name of the BigQuery dataset for silver layer"
  type        = string
  default     = "silver2_dataset"
}

variable "bigquery_dataset_gold2" {
  description = "The name of the BigQuery dataset for gold layer"
  type        = string
  default     = "gold2_dataset"
}

variable "project_id" {
  type = string
}
