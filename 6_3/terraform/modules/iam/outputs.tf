output "role_arn" {
  value = aws_iam_role.this.arn
}

output "lambda_sqs_policy_arn" {
  description = "The ARN of the IAM policy allowing Lambda to send messages to SQS"
  value       = aws_iam_policy.lambda_sqs_policy.arn
}
