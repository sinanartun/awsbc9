variable "role_name" {
  description = "The name of the IAM role for Lambda"
  type        = string
}

variable "assume_role_policy" {
  description = "The assume role policy document"
  type        = string
}

variable "policy_arns" {
  description = "A list of policy ARNs to attach to the IAM role"
  type        = list(string)
}

variable "sqs_queue_arn" {
  description = "The ARN of the SQS queue"
  type        = string
}
