# Resume Infrastructure as Code (IaC)

## Overview
This repository, `resume-iac-public`, contains an AWS CloudFormation template to provision the infrastructure for a secure, two-part static resume website hosted on AWS. The setup includes:

- **Private S3 Bucket (`ching-resume-html`)**: Stores the HTML resume content, accessible only via temporary pre-signed URLs.
- **Public S3 Bucket (`ching-resume-auth-page`)**: Hosts a static password form for user authentication.
- **API Gateway and Lambda**: Handles authentication logic, validates user input from the password form, and generates pre-signed URLs for temporary access to the private bucket.
- **GitHub Actions Integration**: Automates deployment of content to both S3 buckets when changes are pushed to the `main` branch of the `resume-site-private` repository.

This repository is public to share the infrastructure setup, while the website content remains private in the `resume-site-private` repository.

## Project Goals
- Securely host a private resume website on AWS S3 with password-protected access.
- Provide a public authentication page to collect and validate user credentials.
- Use AWS API Gateway and Lambda to manage secure access via pre-signed URLs.
- Automate deployments using GitHub Actions for seamless updates.
- Define all infrastructure using Infrastructure as Code (IaC) for reproducibility and scalability.

## Repository Contents
- `cloudformation-template.yml`: AWS CloudFormation template to provision:
  - A private S3 bucket (`ching-resume-html`) for resume content.
  - A public S3 bucket (`ching-resume-auth-page`) for the authentication form.
  - An AWS Lambda function to validate passwords and generate pre-signed URLs.
  - An API Gateway REST API to handle authentication requests.
  - Necessary IAM roles and policies for secure access.

## CloudFormation Template Details
The CloudFormation template (`cloudformation-template.yml`) performs the following:
- Creates a private S3 bucket (`ching-resume-html`) for hosting resume HTML and CSS files, with no public access.
- Creates a public S3 bucket (`ching-resume-auth-page`) configured for static website hosting, serving a password form (`index.html`).
- Provisions a Lambda function to validate user-submitted passwords and generate pre-signed URLs for accessing files in the private bucket.
- Sets up an API Gateway REST API to receive password form submissions and invoke the Lambda function.
- Configures IAM roles and policies to allow:
  - Lambda to generate S3 pre-signed URLs.
  - API Gateway to invoke the Lambda function.
  - GitHub Actions to upload files to both S3 buckets.
- Outputs key information, such Hawkins:
  - The website endpoint for the public authentication page.
  - The API Gateway endpoint for form submissions.
  - The private bucket name for reference.

## Deployment Instructions
1. **Clone the Repository**: Clone this public repository locally.
2. **Deploy the CloudFormation Stack**:
   - Navigate to the AWS CloudFormation console.
   - Create a new stack and upload `cloudformation-template.yml`.
   - Specify a stack name (e.g., `ResumeSiteStack`) and provide required parameters (see below for details).
   - Deploy the stack and wait for completion.
3. **Verify Resources**:
   - Check the S3 buckets (`ching-resume-html` and `ching-resume-auth-page`) in the AWS S3 console.
   - Access the public bucket’s website endpoint to verify the authentication form loads.
   - Test the API Gateway endpoint to ensure the Lambda function processes requests and returns pre-signed URLs.
4. **Integrate with Website Repository**:
   - Update the `resume-site-private` repository’s GitHub Actions workflow to deploy HTML/CSS files to `ching-resume-html` and the authentication form to `ching-resume-auth-page`.

## Parameters for CloudFormation Template
To deploy the CloudFormation stack, provide the following parameters:
- **PrivateBucketName**: Name of the private S3 bucket (default: `ching-resume-html`).
- **PublicBucketName**: Name of the public S3 bucket (default: `ching-resume-auth-page`).
- **AWSRegion**: AWS region for deployment (e.g., `us-east-1`).
- **LambdaFunctionName**: Name for the Lambda function (e.g., `ResumeAuthFunction`).
- **APIGatewayName**: Name for the API Gateway REST API (e.g., `ResumeAuthAPI`).
- **Password**: A secure password for validating user input (stored securely in AWS Systems Manager Parameter Store).
- **PreSignedURLExpiration**: Duration (in seconds) for pre-signed URL validity (e.g., `3600` for 1 hour).

## Prerequisites
- An AWS account with permissions to create CloudFormation stacks, S3 buckets, Lambda functions, API Gateway, IAM roles, and Systems Manager parameters.
- The `resume-site-private` repository configured with GitHub Actions for deploying to both S3 buckets.
- AWS CLI (optional) for local testing and deployment.

## Related Repository
- **[resume-site-private](https://github.com/your-username/resume-site-private)**: Private repository containing the resume HTML/CSS files and the authentication form, deployed to the respective S3 buckets.

## License
This repository is public and licensed under the MIT License. Feel free to use the CloudFormation template as a reference for similar secure static website projects.