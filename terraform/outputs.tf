output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.finpilot.id
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "cluster_id" {
  description = "The name/id of the EKS cluster"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS control plane"
  value       = module.eks.cluster_security_group_id
}

output "node_security_group_id" {
  description = "Security group ID attached to the worker nodes"
  value       = aws_security_group.eks_nodes.id
}

output "configure_kubectl" {
  description = "CLI command to update local kubeconfig for EKS"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}
