variable "region" {
  description = "The AWS region to deploy in"
  type        = string
}

variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "runtime" {
  description = "The runtime environment for the Lambda function"
  type        = string
}

variable "role_arn" {
  description = "The ARN of the IAM role that Lambda assumes when it executes your function"
  type        = string
}

variable "handler" {
  description = "The function entrypoint in your code"
  type        = string
}

variable "filename" {
  description = "The path to the deployment package for the Lambda function"
  type        = string
}

variable "environment_variables" {
  description = "A map of environment variables to pass to the Lambda function"
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "A map of tags to assign to the resource"
  type        = map(string)
  default     = {}
}

variable "api_gateway_arn" {
  description = "The ARN of the API Gateway that will trigger the Lambda function"
  type        = string
}
