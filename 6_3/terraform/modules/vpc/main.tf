provider "aws" {
  region = var.region
}

resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = var.vpc_name
  }
}

resource "aws_subnet" "public" {
  count = 3
  vpc_id = aws_vpc.this.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index)
  map_public_ip_on_launch = true
  availability_zone = element(var.availability_zones, count.index)

  tags = {
    Name = format("%s-public-subnet-%d", var.vpc_name, count.index + 1)
  }
}
