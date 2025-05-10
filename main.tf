terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.31.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-study-457716-terra-bucket"
  location      = "Asia"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}