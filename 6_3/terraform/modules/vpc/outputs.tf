output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.this.id
}

output "public_subnets" {
  description = "The IDs of the public subnets"
  value       = aws_subnet.public[*].id
}
