terraform {
  backend "s3" {
    region  = "eu-west-1"
    bucket  = "068167017169-terraform-state"
    key     = "cicd.tfstate"
    encrypt = true
  }
}

provider "aws" {
  region  = "eu-west-1"
  profile = "bedrock"
}

data "aws_iam_policy_document" "trust" {
  statement {
    sid    = "TrustGitHub"
    effect = "Allow"
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:malekmaciej/przepisy:*"]
    }
    actions = ["sts:AssumeRoleWithWebIdentity"]
  }
}

resource "aws_iam_role" "github_actions_demo" {
  name               = "przepisy-cicd-role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy_attachment" "admin" {
  role       = aws_iam_role.github_actions_demo.name
  policy_arn = aws_iam_policy.allow_actions.arn
}

resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1", "1c58a3a8518e8759bf075b76b750d4f2df264fcd"]
  client_id_list  = ["sts.amazonaws.com"]
}
# Policy to allow upload to S3 bucket and start Bedrock ingestion job
resource "aws_iam_policy" "allow_actions" {
  name        = "AllowActionsPolicy"
  description = "Policy to allow S3 upload and Bedrock ingestion job start"
  policy      = data.aws_iam_policy_document.allow_actions.json

}

data "aws_iam_policy_document" "allow_actions" {
  statement {
    sid    = "AllowS3Upload"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
    ]
    resources = [
      "arn:aws:s3:::cookbook-recipes-068167017169/*",
    ]
  }
  statement {
    sid    = "AllowBedrockIngestion"
    effect = "Allow"
    actions = [
      "bedrock:StartIngestionJob",
    ]
    resources = [
      "arn:aws:bedrock:us-east-1:068167017169:knowledge-base/XK7TH8KBIF",
      "arn:aws:bedrock:us-east-1:068167017169:data-source/6L0ICMK6TX",
    ]
  }
}
