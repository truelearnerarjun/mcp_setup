# Bedrock Setup Guide

## Fixed Issues

This guide documents the Bedrock integration fixes and setup requirements.

### Issues Fixed

1. ✅ **API Request Format** - Changed from raw text to proper JSON format with `inputText` field
2. ✅ **Response Parsing** - Added proper JSON parsing to extract `outputText` from response
3. ✅ **Client Configuration** - Changed from `bedrock` to `bedrock-runtime` client
4. ✅ **Environment Variables** - Added to `deployment.yaml`
5. ✅ **AWS Authentication** - Added IAM RBAC configuration

## Setup Steps

### 1. Update AWS Account ID (Required)
Edit [rbac.yaml](rbac.yaml) and replace `ACCOUNT_ID` with your AWS account ID and `REGION` with your AWS region.

### 2. Create IAM Role (One-time Setup)

Run these commands to set up the IAM role for EKS service account:

```bash
# Replace ACCOUNT_ID, REGION, and OIDC_ID with your values
ACCOUNT_ID="your-account-id"
REGION="us-east-1"
OIDC_ID=$(aws eks describe-cluster --name your-cluster-name --region $REGION --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)

# Create trust policy
cat > /tmp/trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$ACCOUNT_ID:oidc-provider/oidc.eks.$REGION.amazonaws.com/id/$OIDC_ID"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.$REGION.amazonaws.com/id/$OIDC_ID:sub": "system:serviceaccount:default:mcp-server"
        }
      }
    }
  ]
}
EOF

# Create the IAM role
aws iam create-role \
  --role-name mcp-server-bedrock-role \
  --assume-role-policy-document file:///tmp/trust-policy.json
```

### 3. Add Bedrock Permissions (One-time Setup)

```bash
# Create policy for Bedrock access
cat > /tmp/bedrock-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:$REGION:$ACCOUNT_ID:foundation-model/*"
    }
  ]
}
EOF

# Attach policy to role
aws iam put-role-policy \
  --role-name mcp-server-bedrock-role \
  --policy-name bedrock-invoke \
  --policy-document file:///tmp/bedrock-policy.json
```

### 4. Deploy Service Account and RBAC

```bash
kubectl apply -f mcp-server/rbac.yaml
```

### 5. Deploy MCP Server

```bash
kubectl apply -f mcp-server/deployment.yaml
kubectl apply -f mcp-server/service.yaml
```

### 6. Verify Deployment

```bash
# Check pod is running
kubectl get pods -l app=mcp-server

# Check logs
kubectl logs -l app=mcp-server

# Test the endpoint
kubectl port-forward svc/mcp-server 8000:8000
curl http://localhost:8000/tools
```

## Testing Bedrock Integration

Once deployed, test the Bedrock text generator:

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "bedrock_text_generator",
    "input": "Hello, what is machine learning?"
  }'
```

Expected successful response:
```json
{
  "tool": "bedrock_text_generator",
  "model_id": "amazon.titan-text-2",
  "response": "Machine learning is..."
}
```

## Environment Variables

- `AWS_REGION` - AWS region (default: us-east-1)
- `BEDROCK_MODEL_ID` - Bedrock model to use (default: amazon.titan-text-2)
- `BEDROCK_ENABLED` - Enable Bedrock integration (default: true)

## Troubleshooting

### "Bedrock call failed" Error
- Check IAM role permissions
- Verify OIDC trust relationship is correct
- Confirm Bedrock is available in your region

### "Model not available" Error
- Verify you have access to the Bedrock model
- Check you've accepted model access in AWS Console

### Pod pending/CrashLoopBackOff
- Check service account is created: `kubectl get sa mcp-server`
- Check IAM role annotation is correct
- Review pod logs for specific errors
