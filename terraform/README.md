# FinPilot Infrastructure as Code (Terraform)

This directory provisions the complete AWS infrastructure for the FinPilot DevOps Capstone project using Terraform.

## Architecture Provisioned

1. **Virtual Private Cloud (VPC)**
   - CIDR: `10.0.0.0/16`
   - 3 Public Subnets across 3 Availability Zones (with Internet Gateway)
   - 3 Private Subnets across 3 Availability Zones (with NAT Gateways for outbound security)
   - Proper Kubernetes tags (`kubernetes.io/cluster/finpilot-eks = shared`, `kubernetes.io/role/elb = 1`, `kubernetes.io/role/internal-elb = 1`)

2. **Amazon EKS Cluster**
   - Version: `1.31`
   - Public and Private endpoint access
   - Core add-ons: CoreDNS, Kube-Proxy, VPC-CNI
   - Managed Node Group with auto-scaling (1-4 nodes, desired 2x `t3.medium`)
   - IAM Roles & Least-privilege Policies

## Prerequisites

- [AWS CLI v2](https://aws.amazon.com/cli/) configured with `aws configure` (Region: `ap-south-1`)
- [Terraform >= 1.9.0](https://www.terraform.io/downloads.html)
- [kubectl >= 1.30](https://kubernetes.io/docs/tasks/tools/)

## Deployment Lifecycle

```bash
# 1. Format check
terraform fmt -check

# 2. Initialize modules and providers
terraform init

# 3. Validate syntax and arguments
terraform validate

# 4. Generate and inspect execution plan
terraform plan -var-file="terraform.tfvars.example" -out=tfplan

# 5. Apply infrastructure (Authorization required)
terraform apply tfplan

# 6. Retrieve cluster kubeconfig
aws eks update-kubeconfig --region ap-south-1 --name finpilot-eks

# 7. Verify cluster connectivity
kubectl get nodes -o wide

# 8. Clean up infrastructure when done (prevents unexpected AWS charges)
terraform destroy -auto-approve
```

> [!CAUTION]
> Running `terraform apply` provisions live AWS EC2, NAT Gateways, and EKS resources that incur billing. Always run `terraform destroy` when your evaluation is complete.
