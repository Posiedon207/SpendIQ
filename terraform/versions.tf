terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.34"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.16"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }

  # Uncomment and configure for remote state in production:
  # backend "s3" {
  #   bucket         = "finpilot-terraform-state"
  #   key            = "eks/terraform.tfstate"
  #   region         = "ap-south-1"
  #   encrypt        = true
  #   dynamodb_table = "finpilot-terraform-locks"
  # }
}
