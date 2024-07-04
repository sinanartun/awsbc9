output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "The IDs of the public subnets"
  value       = module.vpc.public_subnets
}

output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = module.lambda.lambda_function_name
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = module.lambda.lambda_function_arn
}

output "iam_role_arn" {
  description = "The ARN of the IAM role"
  value       = module.iam.role_arn
}

output "sqs_queue_url" {
  description = "The URL of the SQS queue"
  value       = module.sqs.sqs_queue_url
}

output "sqs_queue_arn" {
  description = "The ARN of the SQS queue"
  value       = module.sqs.sqs_queue_arn
}

output "kinesis_stream_name" {
  description = "The name of the Kinesis stream"
  value       = module.kinesis.kinesis_stream_name
}

output "kinesis_stream_arn" {
  description = "The ARN of the Kinesis stream"
  value       = module.kinesis.kinesis_stream_arn
}
