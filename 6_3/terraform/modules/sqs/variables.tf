variable "queue_name" {
  description = "The name of the SQS queue"
  type        = string
}

variable "visibility_timeout_seconds" {
  description = "The visibility timeout for the queue"
  type        = number
  default     = 60
}

variable "message_retention_seconds" {
  description = "The number of seconds for which Amazon SQS retains a message"
  type        = number
  default     = 3600  # 1 hour
}

variable "tags" {
  description = "A map of tags to assign to the queue"
  type        = map(string)
  default     = {}
}
