variable "region" {
  description = "The AWS region to deploy in"
  type        = string
  default     = "eu-north-1"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_name" {
  description = "The name of the VPC"
  type        = string
  default     = "my-vpc"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["eu-north-1a", "eu-north-1b", "eu-north-1c"]
}

variable "lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
  default     = "step_1"
}

variable "lambda_runtime" {
  description = "The runtime environment for the Lambda function"
  type        = string
  default     = "python3.12"
}

variable "lambda_role_arn" {
  description = "The ARN of the IAM role that Lambda assumes when it executes your function"
  type        = string
}

variable "lambda_handler" {
  description = "The function entrypoint in your code"
  type        = string
  default     = "index.handler"
}

variable "lambda_filename" {
  description = "The path to the deployment package for the Lambda function"
  type        = string
}

variable "lambda_environment_variables" {
  description = "A map of environment variables to pass to the Lambda function"
  type        = map(string)
  default     = {}
}

variable "lambda_tags" {
  description = "A map of tags to assign to the Lambda function"
  type        = map(string)
  default     = {}
}

variable "lambda_api_gateway_arn" {
  description = "The ARN of the API Gateway that will trigger the Lambda function"
  type        = string
}

variable "iam_role_name" {
  description = "The name of the IAM role"
  type        = string
}

variable "iam_policy_name" {
  description = "The name of the IAM policy"
  type        = string
}

variable "iam_tags" {
  description = "A map of tags to assign to the IAM resources"
  type        = map(string)
  default     = {}
}

variable "sqs_queue_name" {
  description = "The name of the SQS queue"
  type        = string
}

variable "sqs_visibility_timeout" {
  description = "The visibility timeout for the SQS queue"
  type        = number
  default     = 30
}

variable "sqs_message_retention_seconds" {
  description = "The message retention period for the SQS queue"
  type        = number
  default     = 345600
}

variable "sqs_delay_seconds" {
  description = "The time in seconds that the delivery of all messages in the SQS queue will be delayed"
  type        = number
  default     = 0
}

variable "sqs_max_message_size" {
  description = "The limit of how many bytes a message can contain before Amazon SQS rejects it"
  type        = number
  default     = 262144
}

variable "sqs_tags" {
  description = "A map of tags to assign to the SQS queue"
  type        = map(string)
  default     = {}
}

variable "kinesis_stream_name" {
  description = "The name of the Kinesis stream"
  type        = string
  default     = "bist"
}

variable "kinesis_shard_count" {
  description = "The number of shards that the stream uses"
  type        = number
  default     = 1
}

variable "kinesis_retention_period" {
  description = "The number of hours for the data records that are stored in shards to remain accessible"
  type        = number
  default     = 24
}

variable "kinesis_shard_level_metrics" {
  description = "List of shard-level CloudWatch metrics which you want to enable for the stream"
  type        = list(string)
  default     = []
}

variable "kinesis_tags" {
  description = "A map of tags to assign to the Kinesis stream"
  type        = map(string)
  default     = {}
}
