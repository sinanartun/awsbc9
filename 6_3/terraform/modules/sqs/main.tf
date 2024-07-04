provider "aws" {
  region = var.region
}

resource "aws_sqs_queue" "this" {
  name                      = var.queue_name
  visibility_timeout_seconds = var.visibility_timeout
  message_retention_seconds = var.message_retention_seconds
  delay_seconds             = var.delay_seconds
  max_message_size          = var.max_message_size
  tags                      = var.tags
}
