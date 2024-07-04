variable "region" {
  description = "The AWS region to deploy in"
  type        = string
}

variable "stream_name" {
  description = "The name of the Kinesis stream"
  type        = string
  default     = "bist"
}

variable "shard_count" {
  description = "The number of shards that the stream uses"
  type        = number
  default     = 1
}

variable "retention_period" {
  description = "The number of hours for the data records that are stored in shards to remain accessible"
  type        = number
  default     = 24
}

variable "shard_level_metrics" {
  description = "List of shard-level CloudWatch metrics which you want to enable for the stream"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "A map of tags to assign to the resource"
  type        = map(string)
  default     = {}
}
