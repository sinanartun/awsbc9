output "lambda_function_arns" {
  description = "The ARNs of the Lambda functions"
  value       = module.lambda.lambda_function_arns
}

output "lambda_function_names" {
  description = "The names of the Lambda functions"
  value       = module.lambda.lambda_function_names
}

output "lambda_role_arn" {
  value = module.iam.role_arn
}

output "public_subnets" {
  value = module.vpc.public_subnets
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
