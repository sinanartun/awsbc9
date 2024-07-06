output "lambda_function_arns" {
  description = "The ARNs of the Lambda functions"
  value       = [for lambda in aws_lambda_function.this : lambda.arn]
}

output "lambda_function_names" {
  description = "The names of the Lambda functions"
  value       = [for lambda in aws_lambda_function.this : lambda.function_name]
}
