provider "google" {
  credentials = file("<path-to-your-service-account-key>.json")
  project     = var.project_id
  region      = var.region
}

resource "google_bigquery_dataset" "silver" {
  dataset_id = "${var.project_id}_silver"
  location   = var.region
}

resource "google_bigquery_dataset" "gold" {
  dataset_id = "${var.project_id}_gold"
  location   = var.region
}

resource "google_bigquery_table" "silver_table" {
  dataset_id = google_bigquery_dataset.silver.dataset_id
  table_id   = "your_silver_table"
  schema     = file("path/to/your/silver_table_schema.json")
}

resource "google_bigquery_table" "gold_table" {
  dataset_id = google_bigquery_dataset.gold.dataset_id
  table_id   = "your_gold_table"
  schema     = file("path/to/your/gold_table_schema.json")
}

output "silver_dataset_id" {
  value = google_bigquery_dataset.silver.dataset_id
}

output "gold_dataset_id" {
  value = google_bigquery_dataset.gold.dataset_id
}