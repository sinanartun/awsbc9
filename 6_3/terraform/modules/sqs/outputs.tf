output "queue_url" {
  description = "The URL of the created SQS queue"
  value       = aws_sqs_queue.this.url
}

output "queue_arn" {
  description = "The ARN of the created SQS queue"
  value       = aws_sqs_queue.this.arn
}
