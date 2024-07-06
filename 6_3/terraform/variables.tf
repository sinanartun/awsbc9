variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "A list of CIDR blocks for the public subnets"
  type        = list(string)
  default     = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]
}

variable "lambda_role_name" {
  description = "The name of the IAM role for Lambda"
  type        = string
  default     = "lambda_execution_role"
}

variable "assume_role_policy" {
  description = "assume_role_policy for Lambda"
  type        = string

  default = <<JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
JSON
}


variable "lambda_policy_arns" {
  description = "A list of policy ARNs to attach to the Lambda execution role"
  type        = list(string)
  default     = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
}

variable "windows_paths" {
  description = "Paths for Windows OS"
  type = map(object({
    source_file = string
    source_zip  = string
  }))
  default = {
    step1 = {
      source_file = "modules\\lambda\\code\\step1\\lambda_function.py"
      source_zip  = "modules\\lambda\\code\\step1\\lambda_function.zip"
    }
    step3 = {
      source_file = "modules\\lambda\\code\\step3\\lambda_function.py"
      source_zip  = "modules\\lambda\\code\\step3\\lambda_function.zip"
    }
  }
}

variable "linux_paths" {
  description = "Paths for Linux and macOS"
  type = map(object({
    source_file = string
    source_zip  = string
  }))
  default = {
    step1 = {
      source_file = "modules/lambda/code/step1/lambda_function.py"
      source_zip  = "modules/lambda/code/step1/lambda_function.zip"
    }
    step3 = {
      source_file = "modules/lambda/code/step3/lambda_function.py"
      source_zip  = "modules/lambda/code/step3/lambda_function.zip"
    }
  }
}

variable "lambda_functions" {
  description = "A list of Lambda function configurations"
  type = list(object({
    function_name = string
    handler       = string
    runtime       = string
    timeout       = number
  }))
  default = [
    {
      function_name = "step1"
      handler       = "lambda_function.lambda_handler"
      runtime       = "python3.12"
      timeout       = 60
    },
    {
      function_name = "step3"
      handler       = "lambda_function.lambda_handler"
      runtime       = "python3.12"
      timeout       = 60
    }
  ]
}

variable "environment_variables_default" {
  description = "Default environment variables for Lambda functions"
  type        = map(string)
  default     = {}
}

variable "sqs_queue_name" {
  description = "The name of the SQS queue"
  type        = string
  default     = "step2"
}

variable "sqs_visibility_timeout_seconds" {
  description = "The visibility timeout for the queue"
  type        = number
  default     = 65
}

variable "sqs_message_retention_seconds" {
  description = "The number of seconds for which Amazon SQS retains a message"
  type        = number
  default     = 3600  # 1 hour
}

variable "sqs_tags" {
  description = "A map of tags to assign to the queue"
  type        = map(string)
  default     = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}
