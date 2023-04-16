variable "project_id" {
  description = "The ID of the GCP project to manage resources in."
  type        = string
}

variable "dataset_id" {
  description = "The ID of the Dataset"
  type        = string
  default     = "greenery"
}
