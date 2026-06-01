output "load_balancer_dns" {
  description = "Public DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "app_url" {
  description = "Application URL"
  value       = "http://${aws_lb.main.dns_name}"
}

output "s3_bucket_name" {
  description = "Name of the S3 assets bucket"
  value       = aws_s3_bucket.app_assets.bucket
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "ec2_instance_ids" {
  description = "IDs of the EC2 instances"
  value       = [aws_instance.app_a.id, aws_instance.app_b.id]
}
