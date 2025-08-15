provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_bigquery_dataset" "silver" {
  dataset_id = "${replace(var.project_id, "-", "_")}_silver"
  location   = var.region
}

resource "google_bigquery_dataset" "gold" {
  dataset_id = "${replace(var.project_id, "-", "_")}_gold"
  location   = var.region
}

