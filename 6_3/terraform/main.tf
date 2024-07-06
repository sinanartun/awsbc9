locals {
  is_linux   = length(regexall("/home/", lower(abspath(path.root)))) > 0
  is_windows = length(regexall("c:\\\\", lower(abspath(path.root)))) > 0
  is_macos   = length(regexall("/users/", lower(abspath(path.root)))) > 0

  os_type = (
    local.is_linux || local.is_macos ? "linux" :
    local.is_windows ? "windows" :
    "unknown"
  )

  os_paths = (
    local.os_type == "windows" ? var.windows_paths :
    var.linux_paths
  )

  lambda_functions = [
    for fn in var.lambda_functions : {
      function_name = fn.function_name
      handler       = fn.handler
      runtime       = fn.runtime
      source_file   = local.os_paths[fn.function_name].source_file
      source_zip    = local.os_paths[fn.function_name].source_zip
      timeout       = fn.timeout
      environment_variables = (
        fn.function_name == "step1" ? merge(
          var.environment_variables_default,
          { SQS_URL = module.sqs.queue_url }
        ) :
        var.environment_variables_default
      )
    }
  ]
}

module "vpc" {
  source              = "./modules/vpc"
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
}

module "sqs" {
  source                    = "./modules/sqs"
  queue_name                = var.sqs_queue_name
  visibility_timeout_seconds = var.sqs_visibility_timeout_seconds
  message_retention_seconds = var.sqs_message_retention_seconds
  tags                      = var.sqs_tags
}

module "iam" {
  source             = "./modules/iam"
  role_name          = var.lambda_role_name
  assume_role_policy = var.assume_role_policy
  policy_arns        = var.lambda_policy_arns
  sqs_queue_arn      = module.sqs.queue_arn
}

module "lambda" {
  source           = "./modules/lambda"
  lambda_functions = local.lambda_functions
  lambda_role_arn  = module.iam.role_arn
  os_type          = local.os_type
  sqs_queue_arn    = module.sqs.queue_arn
  depends_on = [ module.sqs ]
}
