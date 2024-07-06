variable "lambda_functions" {
  description = "A list of Lambda function configurations"
  type = list(object({
    function_name          = string
    handler                = string
    runtime                = string
    source_file            = string
    source_zip             = string
    timeout                = number
    environment_variables  = map(string)
  }))
}

variable "lambda_role_arn" {
  description = "The ARN of the IAM role to attach to the Lambda functions"
  type        = string
}

variable "os_type" {
  description = "The operating system type"
  type        = string
}

variable "sqs_queue_arn" {
  description = "The ARN of the SQS queue"
  type        = string
}