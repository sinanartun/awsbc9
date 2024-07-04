provider "aws" {
  region = var.region
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name
  runtime       = var.runtime
  role          = var.role_arn
  handler       = var.handler
  filename      = var.filename

  environment {
    variables = var.environment_variables
  }

  tags = var.tags
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = var.api_gateway_arn
}
