output "role_arn" {
  description = "The ARN of the IAM role"
  value       = aws_iam_role.lambda_execution.arn
}
