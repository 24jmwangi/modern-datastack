provider "google" {
  credentials = file("${pathexpand("~")}/gcp-key.json")
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

