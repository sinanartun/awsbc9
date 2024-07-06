resource "aws_sqs_queue" "this" {
  name                      = var.queue_name
  visibility_timeout_seconds = var.visibility_timeout_seconds
  message_retention_seconds = var.message_retention_seconds

  tags = var.tags
}
