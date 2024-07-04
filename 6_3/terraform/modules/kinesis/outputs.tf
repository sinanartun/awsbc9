output "kinesis_stream_name" {
  description = "The name of the Kinesis stream"
  value       = aws_kinesis_stream.this.name
}

output "kinesis_stream_arn" {
  description = "The ARN of the Kinesis stream"
  value       = aws_kinesis_stream.this.arn
}
