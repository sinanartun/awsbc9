resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = var.assume_role_policy

  tags = {
    Name = var.role_name
  }
}

resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "${var.role_name}-sqs-policy"
  description = "IAM policy for Lambda to send and receive messages from SQS"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl"
        ],
        Effect   = "Allow",
        Resource = var.sqs_queue_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_policy_attachment" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
}

resource "aws_iam_role_policy_attachment" "default" {
  for_each = toset(var.policy_arns)
  role     = aws_iam_role.this.name
  policy_arn = each.value
}
