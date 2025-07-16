# Resume Infrastructure as Code (IaC)

## Overview
This repository, `resume-iac-public`, contains an AWS CloudFormation template to provision the infrastructure for hosting a static resume website on AWS S3. The template sets up an S3 bucket configured for static website hosting, including public read access and necessary permissions. This repository is public to share the infrastructure setup while keeping the website content private in the `resume-site-private` repository.

## Project Goals
- Define the AWS infrastructure for a static website using Infrastructure as Code (IaC).
- Provision an S3 bucket with static website hosting enabled.
- Ensure public access for website content while maintaining security best practices.
- Support automated deployments from the `resume-site-private` repository.

## Repository Contents
- `cloudformation-template.yml`: AWS CloudFormation template to create the S3 bucket and configure it for static website hosting.

## CloudFormation Template Details
The CloudFormation template (`cloudformation-template.yml`) performs the following:
- Creates an S3 bucket with a unique name (e.g., `resume-site-2025`).
- Configures the bucket for static website hosting with `index.html` as the index document and `error.html` as the error document.
- Applies a bucket policy to allow public read access to objects (`s3:GetObject`).
- Outputs the S3 bucket website endpoint for easy access.

## Deployment Instructions
1. **Clone the Repository**: Clone this public repository locally.
2. **Deploy the CloudFormation Stack**:
   - Go to the AWS CloudFormation console.
   - Create a new stack and upload `cloudformation-template.yml`.
   - Specify a stack name (e.g., `ResumeSiteStack`) and any required parameters.
   - Deploy the stack and wait for completion.
3. **Verify Resources**:
   - Check the S3 bucket in the AWS S3 console.
   - Access the website endpoint provided in the stack outputs.
4. **Integrate with Website Repository**:
   - Ensure the `resume-site-private` repository’s GitHub Actions workflow references the S3 bucket created by this template.

## Prerequisites
- An AWS account with permissions to create CloudFormation stacks, S3 buckets, and IAM policies.
- The `resume-site-private` repository configured with GitHub Actions for deployment.

## License
This repository is public and licensed under the MIT License. Feel free to use the CloudFormation template as a reference for similar projects.