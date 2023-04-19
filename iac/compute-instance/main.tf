resource "google_service_account" "deb-vm" {
  account_id   = "deb-vm"
  display_name = "DEB Service Account for VM"
  project      = "dataengineercafe"
}

resource "google_compute_address" "static" {
  address_type = "EXTERNAL"
  name         = "ipv4-address"
  project      = "dataengineercafe"
  region       = "asia-southeast1"
}

resource "google_compute_instance" "instance_with_ip" {
  name         = "deb"
  machine_type = "e2-standard-2"
  project      = "dataengineercafe"
  zone         = "asia-southeast1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 100
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }

  service_account {
    email  = google_service_account.deb-vm.email
    scopes = ["cloud-platform"]
  }
}