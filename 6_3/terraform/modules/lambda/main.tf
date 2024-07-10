resource "null_resource" "zip_lambda" {
  count = length(var.lambda_functions)

  provisioner "local-exec" {
    command = <<EOT
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
  source_file = var.lambda_functions[count.index].source_file
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
