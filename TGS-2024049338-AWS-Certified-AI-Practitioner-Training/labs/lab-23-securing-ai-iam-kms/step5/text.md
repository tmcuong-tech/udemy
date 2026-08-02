# Step 5 — Keep AI traffic off the public internet with VPC endpoints

Your data is encrypted at rest and in transit. But when an application in your VPC calls Bedrock, the request leaves your VPC, traverses an internet gateway or NAT gateway, and reaches a public AWS endpoint. It is encrypted the whole way — yet many regulated organisations still cannot accept it, because the traffic *left the AWS network* and the instance needed a route to the internet at all.

VPC endpoints solve this. There are two kinds and the exam tests the difference.

| | Gateway endpoint | Interface endpoint (AWS PrivateLink) |
|---|---|---|
| Services supported | Amazon S3 and DynamoDB only | Most services, including **Bedrock** and **SageMaker** |
| How it works | Adds a route to your route table | Creates an ENI with a private IP in your subnet |
| Cost | **No charge** | **Hourly charge per endpoint per AZ, plus data processing charges** |
| Works from on-premises via VPN/DX | No | Yes |

> **Cost warning:** Interface endpoints bill by the hour for every availability zone in which they are provisioned, whether or not any traffic flows. They are not free tier eligible. If you create one in this step you **must** delete it in Step 6. If you would rather not incur the charge, read through this step and inspect the service names without creating anything — the walkthrough below tells you how.

## Inspect the available AI service endpoints (no charge)

This command lists the endpoint services your Region offers, filtered to Bedrock and SageMaker:

```bash
aws ec2 describe-vpc-endpoint-services \
  --region us-east-1 \
  --query 'ServiceNames[?contains(@, `bedrock`) || contains(@, `sagemaker`)]' \
  --output table
```

You will see service names in the form `com.amazonaws.us-east-1.<service>`. Notice that Bedrock exposes **separate endpoint services for the control plane and the runtime**:

- The control plane service covers management calls — listing models, creating customisation jobs.
- The runtime service covers `InvokeModel` — the actual inference traffic that carries your prompts.

This separation matters. If you privatise only the control plane, your prompts still travel over the public path. Securing an inference workload means creating the **runtime** endpoint.

SageMaker is split even further — the API, runtime, notebook, Studio and feature store each have their own endpoint service. Creating one does not privatise the others.

## Create an interface endpoint (optional — incurs charges)

If you choose to proceed, you need an existing VPC, a subnet and a security group. Find your default VPC:

```bash
aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' --output text
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc-id>" \
  --query 'Subnets[0].SubnetId' --output text
```

Then create the endpoint:

```bash
aws ec2 create-vpc-endpoint \
  --vpc-id <vpc-id> \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids <subnet-id> \
  --security-group-ids <security-group-id> \
  --region us-east-1
```

Record the `VpcEndpointId` — you need it for cleanup.

Two configuration details that are easy to get wrong:

1. **The security group attached to the endpoint must allow inbound HTTPS (port 443) from your application's subnet or security group.** An interface endpoint is an ENI, and ENIs are governed by security groups. If inference calls hang after you create an endpoint, this is almost always why.
2. **Private DNS.** With private DNS enabled (the default for most services), the standard service hostname resolves to the endpoint's private IP inside your VPC. Your application code does not change at all — it keeps calling the normal endpoint and the traffic silently stays private. Private DNS requires `enableDnsSupport` and `enableDnsHostnames` on the VPC.

## Lock it down with an endpoint policy

An interface endpoint accepts a resource policy that constrains what can be reached *through* it:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ],
    "Resource": "arn:aws:bedrock:us-east-1::foundation-model/<model-id>"
  }]
}
```

Combine this with the `aws:SourceVpce` condition from Step 2 and you have a closed loop: the identity policy allows the call only from the endpoint, and the endpoint policy allows only that model. Neither control alone is sufficient; together they are hard to bypass.

## The related SageMaker control

For SageMaker notebook instances there is one more network control worth knowing: **disabling direct internet access**. A notebook created with direct internet access disabled cannot reach the internet unless you route it through a NAT gateway you control, which prevents a data scientist from exfiltrating a training dataset to an arbitrary external host. There is an AWS Config managed rule, `sagemaker-notebook-no-direct-internet-access`, that detects violations — you will meet AWS Config in Lab 25.
