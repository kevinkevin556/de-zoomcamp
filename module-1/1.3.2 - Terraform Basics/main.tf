terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.7.0"
    }
  }
}

provider "google" {
  project     = "terraform-demo-439216"
  region      = "us-central1"
  credentials = "./keys/my-creds.json"
}


resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-439216-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }   
  }
}