provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_bigquery_dataset" "silver2" {
  dataset_id = "${replace(var.project_id, "-", "_")}_silver2"
  location   = var.region
}

resource "google_bigquery_dataset" "gold2" {
  dataset_id = "${replace(var.project_id, "-", "_")}_gold2"
  location   = var.region
}

