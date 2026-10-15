# ─── Data Sources ─────────────────────────────────────────────────────────────

data "aws_availability_zones" "available" {
  state = "available"
}

# ─── VPC ──────────────────────────────────────────────────────────────────────

resource "aws_vpc" "finpilot" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.vpc_name
    # Required tags for EKS to discover subnets
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

# ─── Internet Gateway ─────────────────────────────────────────────────────────

resource "aws_internet_gateway" "finpilot" {
  vpc_id = aws_vpc.finpilot.id

  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

# ─── Public Subnets ───────────────────────────────────────────────────────────

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.finpilot.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-public-${count.index + 1}"
    # Required for EKS to provision external load balancers
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }
}

# ─── Private Subnets (for EKS worker nodes) ───────────────────────────────────

resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.finpilot.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.vpc_name}-private-${count.index + 1}"
    # Required for EKS to provision internal load balancers
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

# ─── Elastic IPs for NAT Gateways ─────────────────────────────────────────────

resource "aws_eip" "nat" {
  count  = length(var.public_subnet_cidrs)
  domain = "vpc"

  tags = {
    Name = "${var.vpc_name}-nat-eip-${count.index + 1}"
  }

  depends_on = [aws_internet_gateway.finpilot]
}

# ─── NAT Gateways (one per AZ for HA) ────────────────────────────────────────

resource "aws_nat_gateway" "finpilot" {
  count = length(var.public_subnet_cidrs)

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "${var.vpc_name}-nat-${count.index + 1}"
  }

  depends_on = [aws_internet_gateway.finpilot]
}

# ─── Public Route Table ───────────────────────────────────────────────────────

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.finpilot.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.finpilot.id
  }

  tags = {
    Name = "${var.vpc_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# ─── Private Route Tables (one per AZ, routes through NAT) ───────────────────

resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.finpilot.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.finpilot[count.index].id
  }

  tags = {
    Name = "${var.vpc_name}-private-rt-${count.index + 1}"
  }
}

resource "aws_route_table_association" "private" {
  count = length(aws_subnet.private)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# ─── Security Groups ──────────────────────────────────────────────────────────

resource "aws_security_group" "eks_cluster" {
  name        = "${var.cluster_name}-cluster-sg"
  description = "Security group for EKS cluster control plane"
  vpc_id      = aws_vpc.finpilot.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.cluster_name}-cluster-sg"
  }
}

resource "aws_security_group" "eks_nodes" {
  name        = "${var.cluster_name}-nodes-sg"
  description = "Security group for EKS worker nodes"
  vpc_id      = aws_vpc.finpilot.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
    description = "Allow all intra-node communication"
  }

  ingress {
    from_port       = 1025
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster.id]
    description     = "Allow control plane to communicate with worker nodes"
  }

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster.id]
    description     = "Allow HTTPS from control plane"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.cluster_name}-nodes-sg"
  }
}
