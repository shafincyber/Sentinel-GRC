provider "aws" { region = "eu-central-1" }

resource "aws_s3_bucket" "ai_training_data" {
  bucket = "shafin-ai-training-data-eu"
}

resource "aws_iam_policy" "restricted_policy" {
  name        = "restricted-access-policy"
  policy      = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "s3:*",
        Effect    = "Allow",
        Resource  = aws_s3_bucket.ai_training_data.arn,
        Condition = {
          StringLike = {
            "aws:PrincipalArn" : ["arn:aws:iam::123456789012:service-account/service-account-1", "arn:aws:iam::123456789012:service-account/service-account-2"]
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "attach-policy" {
  name       = "restricted-access-attachment"
  policy_arn = aws_iam_policy.restricted_policy.arn
  roles      = ["arn:aws:iam::123456789012:role/service-account-execution-role"]
}