provider "aws" {
  region = var.region
}

module "vpc" {
  source             = "./modules/vpc"
  region             = var.region
  vpc_cidr           = var.vpc_cidr
  vpc_name           = var.vpc_name
  availability_zones = var.availability_zones
}

module "iam" {
  source      = "./modules/iam"
  region      = var.region
  role_name   = var.iam_role_name
  policy_name = var.iam_policy_name
  tags        = var.iam_tags
}

module "lambda" {
  source                = "./modules/lambda"
  region                = var.region
  function_name         = var.lambda_function_name
  runtime               = var.lambda_runtime
  role_arn              = module.iam.role_arn
  handler               = var.lambda_handler
  filename              = var.lambda_filename
  environment_variables = var.lambda_environment_variables
  tags                  = var.lambda_tags
  api_gateway_arn       = var.lambda_api_gateway_arn
}

module "sqs" {
  source                    = "./modules/sqs"
  region                    = var.region
  queue_name                = var.sqs_queue_name
  visibility_timeout        = var.sqs_visibility_timeout
  message_retention_seconds = var.sqs_message_retention_seconds
  delay_seconds             = var.sqs_delay_seconds
  max_message_size          = var.sqs_max_message_size
  tags                      = var.sqs_tags
}

module "kinesis" {
  source               = "./modules/kinesis"
  region               = var.region
  stream_name          = var.kinesis_stream_name
  shard_count          = var.kinesis_shard_count
  retention_period     = var.kinesis_retention_period
  shard_level_metrics  = var.kinesis_shard_level_metrics
  tags                 = var.kinesis_tags
}
