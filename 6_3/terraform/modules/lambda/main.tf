# Variables
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

# Main Configuration
resource "null_resource" "zip_lambda" {
  count = length(var.lambda_functions)

  provisioner "local-exec" {
    command = var.os_type == "windows" ? <<EOT
      powershell -Command "Compress-Archive -Path ${var.lambda_functions[count.index].source_file} -DestinationPath ${var.lambda_functions[count.index].source_zip}"
      Start-Sleep -s 5
      if (!(Test-Path -Path ${var.lambda_functions[count.index].source_zip})) {
        Write-Host "File not created: ${var.lambda_functions[count.index].source_zip}"
        exit 1
      }
    EOT : <<EOT
      zip -j ${var.lambda_functions[count.index].source_zip} ${var.lambda_functions[count.index].source_file}
      sleep 5
      if [ ! -f ${var.lambda_functions[count.index].source_zip} ]; then
        echo "File not created: ${var.lambda_functions[count.index].source_zip}"
        exit 1
      fi
    EOT
  }

  triggers = {
    python_file = filemd5(var.lambda_functions[count.index].source_file)
  }
}

data "archive_file" "lambda_zip" {
  count       = length(var.lambda_functions)
  type        = "zip"
  source_file = var.lambda_functions[count.index].source_zip
  output_path = var.lambda_functions[count.index].source_zip
  depends_on  = [null_resource.zip_lambda]
}

resource "aws_lambda_function" "this" {
  count = length(var.lambda_functions)

  function_name    = var.lambda_functions[count.index].function_name
  handler          = var.lambda_functions[count.index].handler
  runtime          = var.lambda_functions[count.index].runtime
  role             = var.lambda_role_arn
  filename         = var.lambda_functions[count.index].source_zip
  source_code_hash = data.archive_file.lambda_zip[count.index].output_base64sha256
  timeout          = var.lambda_functions[count.index].timeout

  environment {
    variables = var.lambda_functions[count.index].environment_variables
  }

  tags = {
    Name = var.lambda_functions[count.index].function_name
  }

  depends_on = [null_resource.zip_lambda]
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  count             = length(var.lambda_functions)
  event_source_arn  = var.sqs_queue_arn
  function_name     = aws_lambda_function.this[count.index].arn
  enabled           = true

  depends_on = [aws_lambda_function.this]
}

# Outputs
output "lambda_function_arns" {
  description = "The ARNs of the Lambda functions"
  value       = [for f in aws_lambda_function.this : f.arn]
}

output "lambda_function_names" {
  description = "The names of the Lambda functions"
  value       = [for f in aws_lambda_function.this : f.function_name]
}

output "lambda_role_arn" {
  description = "The ARN of the IAM role attached to the Lambda functions"
  value       = var.lambda_role_arn
}

output "public_subnets" {
  description = "The IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}
